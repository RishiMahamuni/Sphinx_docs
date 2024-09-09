from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class CosineSimilarityComponent(Component):
    name = "cosine_similarity"
    provides = ["similarity_score"]
    requires = ["text"]
    
    defaults = {
        "word_list": ["trade", "status", "information search"]
    }

    def __init__(self, component_config=None):
        super(CosineSimilarityComponent, self).__init__(component_config)
        self.word_list = component_config.get("word_list", self.defaults['word_list'])

    def train(self, training_data, cfg, **kwargs):
        """Not needed, this component does not require training."""
        pass

    def process(self, message, **kwargs):
        # Get input query text
        input_text = message.get("text")

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
        message.set("similarity_score", {"best_match": self.word_list[best_match_idx], "score": best_match_score})

    def persist(self, file_name, model_dir):
        """Not needed, this component doesn't need persistence."""
        pass
