from Dataset import *
from Classifier import *

from enum import Enum
import numpy as np
import math
import operator
import png
import functools
import colorsys


class gKNN(Classifier):

    def __init__(self, dataset, configuration):
        Classifier.__init__(self, dataset)
        self.k = configuration['k']
        self.g = configuration['g']
        self.d = configuration['d']
        for sample in dataset.source_samples:
            sample.cells = self.featuresToCells(sample.features)

    def featuresToCells(self, features):
        return [int(v*self.g) for v in features]

    # === Learning ===
    def learn(self):
        pass

    def predict(self):
        for sample in self.dataset.test:
            winners = []
            entry_threshold = 2
            cells = self.featuresToCells(sample.features)

            for source in self.dataset.samples:
                cmpCells = self.featuresToCells(source.features)
                comparison = map(abs, (map(operator.sub, cells, cmpCells)))
                shallNotPass = max(comparison) > self.d

                if shallNotPass:
                    continue

                # print "%s vs %s is %s [%i]" % (
                #     str(cells), str(cmpCells), str(comparison), shallNotPass)
                distance = np.linalg.norm(
                    sample.features - source.features)
                if distance < entry_threshold:
                    winners.append((source, distance))

                if len(winners) > self.k:
                    winners.sort(key=lambda distance: distance[1])
                    winners = winners[0:self.k]
                    entry_threshold = winners[-1][1]

            for winner in winners:
                sample.support[winner[0].label] += 1

            sample.decidePrediction()
