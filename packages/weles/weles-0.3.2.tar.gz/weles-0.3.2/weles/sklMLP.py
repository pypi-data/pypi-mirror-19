# Adapter for sklearn
from Dataset import *
from Classifier import *

from sklearn import neural_network

class sklMLP(Classifier):
    def __init__(self, dataset, configuration):
        Classifier.__init__(self,dataset)
        self.clf = neural_network.MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(5, 2),
            random_state=1)

    # === Learning ===
    def learn(self):
        self.clf.fit(self.dataset.X, self.dataset.y)
        pass

    def predict(self):
        predictions = self.clf.predict(self.dataset.testX)
        for idx, val in enumerate(predictions):
            self.dataset.test[idx].prediction = val
