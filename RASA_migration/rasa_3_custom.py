from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.shared.nlu.training_data.message import Message
from rasa.engine.recipes.default_recipe import DefaultV1Recipe

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)
class MyCustomComponent(GraphComponent):
    def __init__(self, config: dict) -> None:
        self.component_config = config

    @classmethod
    def create(
        cls,
        config: dict,
        model_storage: "ModelStorage",
        resource: "Resource",
        execution_context: ExecutionContext,
    ) -> "MyCustomComponent":
        return cls(config)

    def process(self, messages: list[Message]) -> list[Message]:
        for message in messages:
            # Accessing metadata
            metadata = message.get_metadata()

            # For example, getting a specific metadata field
            custom_field = metadata.get("custom_field", "default_value")

            # Use the metadata in your processing logic
            processed_text = f"Processed with metadata: {custom_field}"
            message.set("custom_attribute", processed_text)

        return messages
