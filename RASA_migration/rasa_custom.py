from rasa.engine.graph import GraphComponent
from rasa.shared.nlu.training_data.training_data import TrainingData

class MyCustomComponent(GraphComponent):
    @staticmethod
    def required_components():
        return []

    def __init__(self, config):
        self.config = config

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # Your logic to process training data
        return training_data

    def process(self, message, **kwargs):
        # Your logic to process individual messages
        pass
