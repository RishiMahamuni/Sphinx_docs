from rasa.engine.graph import GraphComponent
from rasa.shared.nlu.training_data.message import Message

class CustomComponent(GraphComponent):
    def __init__(self, config=None):
        self.config = config

    def process(self, messages, **kwargs):
        for message in messages:
            # Custom processing logic
            message.set("my_custom_feature", "value")
        return messages
