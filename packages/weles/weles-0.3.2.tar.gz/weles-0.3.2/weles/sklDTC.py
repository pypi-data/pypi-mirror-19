# Adapter for sklearn
from Dataset import *
from Classifier import *

from sklearn import tree

class sklDTC(Classifier):
    def __init__(self, dataset, configuration):
        Classifier.__init__(self,dataset)
        self.clf = tree.DecisionTreeClassifier()

    # === Learning ===
    def learn(self):
        self.clf.fit(self.dataset.X, self.dataset.y)
        pass

    def predict(self):
        predictions = self.clf.predict(self.dataset.testX)
        for idx, val in enumerate(predictions):
            self.dataset.test[idx].prediction = val
