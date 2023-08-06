import pickle
import os

import edkit_server.edleak.features as features

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Classifier(object):
    def __init__(self):
        self.model = pickle.load( open(os.path.join(__location__,  'edleak-class.pickle'), 'rb' ) )
        return

    def classify(self, dataset):
        """ Classifies each entries of the dataset as 'leak' or 'noleak'
        """
        features.extract_linreg_feature(dataset)
        classification = [ True if self.model.predict(x['linreg_coef'])[0] == True else False for x in dataset ]
        return classification
