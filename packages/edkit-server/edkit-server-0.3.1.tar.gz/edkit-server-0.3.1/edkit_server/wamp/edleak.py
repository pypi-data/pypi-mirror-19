from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

from edkit_server.edleak.classifier import Classifier

class AppSession(ApplicationSession):

    log = Logger()
    edleak_classifier = Classifier()

    @inlineCallbacks
    def onJoin(self, details):

        def classify_dataset(dataset):
            '''
            Classify each entry in the dataset as 'leak' or 'noleak'.

            Parameters:
            - dataset : A list of memory usage list.
            '''
            self.log.info("classify() called")
            return AppSession.edleak_classifier.classify(dataset)

        yield self.register(classify_dataset, 'com.oakbits.edkit.edleak.classify_dataset')
        self.log.info("procedure classify_dataset() registered")
