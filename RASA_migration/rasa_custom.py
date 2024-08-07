# my_custom_component.py

from typing import Dict, Any, List
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

class MyCustomComponent(GraphComponent):
    """A custom NLU component that adds a simple feature to the message."""

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        return {
            "example_param": "default_value"
        }

    def __init__(self, config: Dict[str, Any], name: str, execution_context: ExecutionContext) -> None:
        self.example_param = config.get("example_param", "default_value")

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            # Add a custom attribute to the message
            message.set("my_custom_feature", self.example_param)
        return messages

    def train(self, training_data: TrainingData) -> None:
        """Custom training logic, if any, can be added here."""
        pass
