import keras
from keras import backend as K
import time
import os
import datetime
import numpy as np
import re

from taskProcessors import ProcessTaskProcessor

def parseTrainingProgress(process, line):
    # print(line[:250])
    epochList = re.findall(r'Epoch (\d+)\/(\d+)', line)
    if len(epochList)>0:
        process.task.set('status.stage', 'Epoch '+epochList[-1][0]+'/'+epochList[-1][1])
    progressList = re.findall(r'(\d+)\/(\d+)', line)
    if len(progressList)>0:
        process.task.set('status.progress', int(float(progressList[-1][0])/float(progressList[-1][1])*100))
    etaList = re.findall(r' - ETA: (\d+)s', line)
    totalTimeList = re.findall(r' - (\d+)s', line)
    lossList = re.findall(r' - loss: ([-+]?\d*\.\d+|\d+)', line)
    lossList = re.findall(r' - val_loss: ([-+]?\d*\.\d+|\d+)', line)
    accList = re.findall(r' - acc: ([-+]?\d*\.\d+|\d+)', line)
    process.task.update('status.info', line.replace('\b','')[:150])


class KerasProcess(ProcessTaskProcessor):
    def process_output(self, line):
        try:
            parseTrainingProgress(self,line)
        except Exception as e:
            print('failed to parse output')
            return False
        return True


class ProgressTracker(keras.callbacks.Callback):
    def __init__(self, task):
        self.task = task
        self.start_time = time.time()
        super(ProgressTracker, self).__init__()
        self.task.set('status.progress', 0)

    def on_batch_begin(self, batch, logs={}):
        if self.task.abort.is_set():
            self.task.set('status.error', 'interrupted')
            self.model.stop_training = True
            raise Exception('interrupted')

    def on_batch_end(self, batch, logs={}):
        info = ''
        for k, v in logs.items():
            if isinstance(v, (np.ndarray, np.generic) ):
                vstr = str(v.tolist())
            else:
                vstr = str(v)
            info += "{}: {}\n".format(k,vstr)
        self.elapsed_time = time.time()-self.start_time
        info += "elapsed_time: {:.2f}s".format(self.elapsed_time)
        self.task.update({
            'status.info': info,
            'status.progress': batch%100
        })

    def on_epoch_begin(self, epoch, logs={}):
        self.task.set('status.stage', 'epoch #'+str(epoch))
        if hasattr(self.model.optimizer, 'lr'):
            if self.task.get('config.learning_rate'):
                lr = float(self.task.get('config.learning_rate'))
                K.set_value(self.model.optimizer.lr, lr)
        else:
            self.task.set('status.error', 'Optimizer must have a "lr" attribute.')

    def on_epoch_end(self, epoch, logs={}):
        report = {}
        report['epoch'] = epoch
        for k, v in logs.items():
            report[k] = v
        if hasattr(self.model.optimizer, 'lr'):
            report['lr'] = K.get_value(self.model.optimizer.lr).tolist()
        self.task.push('output.training_history', report)
        self.task.set('output.elapsed_time', "%.2fs"%self.elapsed_time)
        self.task.set('output.last_epoch_update_time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
