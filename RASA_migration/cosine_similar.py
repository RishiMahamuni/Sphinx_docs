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
        input_text = message.get("text")  # Original user query
        entities = message.get("entities", [])  # Extracted entities from the input query

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

        # Process entities, first checking the entity value, and then the original input query if needed
        cleaned_entities = self.clean_entities(entities, input_text)

        # Update message entities with cleaned entities
        message.set("entities", cleaned_entities)

    def clean_entities(self, entities, input_text):
        """Clean the entities based on exact matches and cosine similarity, checking both entity value and input text."""
        cleaned_entities = []
        
        for entity_dict in entities:
            filter_params = entity_dict.get("filter_params", [])
            cleaned_filter_params = []

            for ent in filter_params:
                entity_value = ent.get("value", "")
                if entity_value:
                    cleaned_value, matched_word = self.clean_entity_value(entity_value, input_text)
                    ent["value"] = cleaned_value
                    ent["condition"] = matched_word  # Add matched word to the entity
                cleaned_filter_params.append(ent)

            cleaned_entities.append({"filter_params": cleaned_filter_params})

        return cleaned_entities

    def clean_entity_value(self, entity_value, input_text):
        """Clean the entity value by removing exact matches and similar words, check in value first then query."""
        original_value = entity_value[0]
        entity_value = entity_value[0].lower()  # Normalize to lowercase
        matched_word = None  # To track the word that matched

        # Step 1: Exact word match removal from the entity value
        for word in self.word_list:
            if re.search(rf'\b{word}\b', entity_value):  # If word is found in entity_value
                entity_value = re.sub(rf'\b{word}\b', '', entity_value).strip()
                matched_word = word  # Track the exact matched word
                break  # Break after finding the first match

        # Step 2: If no match is found in the entity value, check the original input text
        if not matched_word:
            matched_word, cleaned_query = self.check_in_query(input_text)

        return entity_value if entity_value else original_value, matched_word  # Return cleaned value and matched word

    def check_in_query(self, input_text):
        """Check the original query text for exact matches and cosine similarity."""
        matched_word = None
        input_text = input_text.lower()  # Normalize input text to lowercase
        cleaned_query = input_text

        # Step 1: Exact word match removal from the query text
        for word in self.word_list:
            if re.search(rf'\b{word}\b', input_text):  # If word is found in input_text
                cleaned_query = re.sub(rf'\b{word}\b', '', input_text).strip()
                matched_word = word  # Track the exact matched word
                break

        # Step 2: If no exact match, check cosine similarity
        if not matched_word:
            corpus = [input_text] + self.word_list
            vectorizer = CountVectorizer().fit_transform(corpus)
            vectors = vectorizer.toarray()

            # Calculate cosine similarity between query text and each word in the list
            cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
            matches = []
            for idx, score in enumerate(cosine_sim[0]):
                if score >= self.similarity_threshold:
                    matches.append(self.word_list[idx])

            # Remove matching words from query text and track the first match
            for match in matches:
                cleaned_query = cleaned_query.replace(match, "").strip()
                matched_word = match  # Track the first similar match
                break

        return matched_word, cleaned_query  # Return the matched word and cleaned query

    def persist(self, model_dir):
        """No need to persist this component."""
        pass
