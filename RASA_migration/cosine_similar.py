from rasa.nlu.components import Component
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


class CosineSimilarityComponent(Component):
    name = "cosine_similarity"
    provides = ["similarity_score"]
    requires = ["text", "entities"]

    defaults = {
        "word_list": ["contains", "equals", "trade", "status", "information search"],
        "similarity_threshold": 0.75  # Threshold for similarity
    }

    def __init__(self, component_config=None):
        super(CosineSimilarityComponent, self).__init__(component_config)
        self.word_list = component_config.get("word_list", self.defaults['word_list'])
        self.similarity_threshold = component_config.get("similarity_threshold", self.defaults['similarity_threshold'])

    def train(self, training_data, cfg, **kwargs):
        """Not needed, this component does not require training."""
        pass

    def process(self, message, **kwargs):
        # Get input query text
        input_text = message.get("text")
        entities = message.get("entities", [])

        # Create corpus of input text and predefined word list
        corpus = [input_text] + self.word_list

        # Vectorize the text using CountVectorizer
        vectorizer = CountVectorizer().fit_transform(corpus)
        vectors = vectorizer.toarray()

        # Calculate cosine similarity between the input query and each word in the list
        cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
        best_match_idx = np.argmax(cosine_sim)
        best_match_score = cosine_sim[0][best_match_idx]

        # Store the best match word and score in the message object
        message.set("similarity_score", {
            "best_match": self.word_list[best_match_idx],
            "score": float(best_match_score)
        })

        # Process entities and remove matching parts based on cosine similarity and exact matching
        cleaned_entities = self.clean_entities(entities)

        # Update message entities
        message.set("entities", cleaned_entities)

    def clean_entities(self, entities):
        """Clean the entities based on exact matches and cosine similarity."""
        cleaned_entities = []
        
        for entity_dict in entities:
            filter_params = entity_dict.get("filter_params", [])
            cleaned_filter_params = []

            for ent in filter_params:
                entity_value = ent.get("value", "")
                if entity_value:
                    cleaned_value = self.clean_entity_value(entity_value)
                    ent["value"] = cleaned_value
                cleaned_filter_params.append(ent)

            cleaned_entities.append({"filter_params": cleaned_filter_params})

        return cleaned_entities

    def clean_entity_value(self, entity_value):
        """Clean the entity value by removing exact matches and similar words."""
        original_value = entity_value
        entity_value = entity_value.lower()  # Normalize to lowercase

        # Step 1: Exact word match removal
        for word in self.word_list:
            entity_value = re.sub(rf'\b{word}\b', '', entity_value).strip()

        # Step 2: If there's still value left, check for cosine similarity
        if entity_value:
            corpus = [entity_value] + self.word_list
            vectorizer = CountVectorizer().fit_transform(corpus)
            vectors = vectorizer.toarray()

            # Calculate cosine similarity between entity value and each word in the list
            cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
            matches = []
            for idx, score in enumerate(cosine_sim[0]):
                if score >= self.similarity_threshold:
                    matches.append(self.word_list[idx])

            # Remove matching words from entity value
            for match in matches:
                entity_value = entity_value.replace(match, "").strip()

        return entity_value if entity_value else original_value  # Return cleaned value or original if empty

    def persist(self, model_dir):
        """No need to persist this component."""
        pass
