import keras
import time

class StatsCallback(keras.callbacks.Callback):

    def __init__(self, model_name):
        super(StatsCallback, self).__init__()
        self.model_name = model_name

    def on_train_begin(self, logs={}):
        self.epoch = []
        self.stats_dict = {}
        self.stats_dict['model_name'] = self.model_name
        self.t0 = time.time()
        self.avg_epoch_time = 0

    def on_train_end(self, logs={}):
        self.t1 = time.time()
        self.train_time = self.t1 - self.t0
        self.stats_dict['train_time'] = self.train_time
        self.stats_dict['epoch_time'] = self.avg_epoch_time

        # Remove not needed members
        del self.t1
        del self.t0
        del self.e1
        del self.e0
 
    def on_epoch_begin(self, epoch, logs={}):
        self.e0 = time.time()
 
    def on_epoch_end(self, epoch, logs={}):
        # Acc and loss history
        self.epoch.append(epoch)
        for k, v in logs.items():
            self.stats_dict.setdefault(k, []).append(v)

        # Time
        self.e1 = time.time()
        epoch_time = self.e1 - self.e0
        if epoch_time != 0:
            self.avg_epoch_time = (self.avg_epoch_time + epoch_time) / 2.0
        else:
            self.avg_epoch_time = epoch_time
 
    def on_batch_begin(self, batch, logs={}):
        return
 
    def on_batch_end(self, batch, logs={}):
        return
