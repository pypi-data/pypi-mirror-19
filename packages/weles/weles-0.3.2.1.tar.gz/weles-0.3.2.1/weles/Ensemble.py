from abc import ABCMeta, abstractmethod
import numpy as np
import random

# To ensure deterministic loop we use randomization with fixed seed.
SEED = 123
random.seed(SEED)

class Ensemble:
    __metaclass__ = ABCMeta
    def __init__(self, dataset):
        # we're gathering the dataset
        self.dataset = dataset



    def quickLoop(self):
        folds = xrange(0,5,1)
        acc = []
        bac = []
        for fold in folds:
            self.dataset.setCV(fold)
            self.learn()
            self.dataset.clearSupports()
            self.predict()
            scores = self.dataset.score()
            acc.append(scores['accuracy'])
            bac.append(scores['bac'])
        acc = np.mean(acc)
        bac = np.mean(bac)
        return {'acc': acc, 'bac': bac}

    @abstractmethod
    def predict():
        pass

    @abstractmethod
    def learn():
        pass
