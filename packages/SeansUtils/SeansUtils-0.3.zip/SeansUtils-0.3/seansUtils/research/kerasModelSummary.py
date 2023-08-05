from __future__ import division, print_function
import keras
from matplotlib import pyplot as plt
import seaborn as sns
import datetime

class ModelSummary(object):
    
    def __init__(self, model, stats):
        self.model = model
        self.stats = stats
        
    def show(self):
        model = self.model
        stats = self.stats
        # Plots
        print(stats['model_name'], '\n--------------------------\n')
        print('MODEL STATS', '\n------------')
        print('Accuracy:'.ljust(15), max(stats['val_acc']))
        print('Loss:'.ljust(15), min(stats['val_loss']))
        print('Parameters:'.ljust(15), model.count_params())
        train_time = str(datetime.timedelta(seconds=stats['train_time']))
        epoch_time = str(datetime.timedelta(seconds=stats['epoch_time']))
        print('Training Time:'.ljust(15), train_time)
        print('Epoch Time:'.ljust(15), epoch_time)

        plt.subplot(121)
        plt.title('Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Number of Epochs')
        plt.plot(stats['acc'])
        plt.plot(stats['val_acc'])
        
        plt.subplot(122)
        plt.title('Loss')
        plt.ylabel('Loss')
        plt.xlabel('Number of Epochs')
        plt.plot(stats['loss'])
        plt.plot(stats['val_loss'])
        
        plt.tight_layout()
        plt.show()
