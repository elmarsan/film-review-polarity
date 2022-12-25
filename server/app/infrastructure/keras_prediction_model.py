from keras import backend as keras_backend
from keras.models import model_from_json
from os.path import join, dirname, realpath
import re
from unicodedata import normalize
import os
import pickle
import numpy as np
from nltk.corpus import stopwords
from os.path import join, dirname, realpath

STOP = stopwords.words('spanish')
TOPICS = 5000
STATIC_PATH = join(dirname(realpath(__file__)), '../../', 'static')
TOPICS_PATH = os.path.join(STATIC_PATH, 'topics')
WEIGHTS_PATH = join(STATIC_PATH, 'model.h5')
JSON_PATH = join(STATIC_PATH, 'model_json')


class KerasPredictionModel:
    """KerasPredictionModel implementation of PredictionModel using keras neural network"""

    def __init__(self) -> None:
        with open(JSON_PATH, 'r') as json_file:
            self.model = model_from_json(json_file.read())
            self.model.load_weights(WEIGHTS_PATH)

        with open(TOPICS_PATH, 'rb') as topics_file:
            self.topics = pickle.load(topics_file)

    def __del__(self):
        keras_backend.clear_session()

    def predict(self, review_body):
        review_body = self.__remove_accents(review_body)
        review_tokens = self.__tokenize(review_body)
        review_tokens = self.__remove_stop_words(review_tokens)
        review_topics = self.__fetch_topics(review_tokens)

        prediction = self.model.predict(self.__pad_sequences(review_topics))

        print(prediction[0][0], prediction[0][0] * 10)
        return round(prediction[0][0] * 10, 1)

    def __remove_accents(self, review_body):
        review_body = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
                             normalize("NFD", review_body), 0, re.I)
        return normalize('NFC', review_body)

    def __tokenize(self, review_body):
        tokens = re.split(r"([-\s.,;!¡'¿?+:)(*@#\"])+", review_body)
        return [char.lower() for char in tokens if char != '' and char not in "- \t\n.,;!¡¿?+:()*@#\""]

    def __remove_stop_words(self, review_body):
        return [word.lower() for word in review_body if word not in STOP]

    def __pad_sequences(self, sequences, dimension=TOPICS):
        results = np.zeros((len(sequences), dimension))
        for i, sequence in enumerate(sequences):
            results[i, sequence] = 1.
        return results

    def __fetch_topics(self, review_body):
        topics_appearance = [[]]

        for token in review_body:
            if token in self.topics:
                topic_number = self.topics[token]
            else:
                topic_number = 0
            topics_appearance[len(topics_appearance) - 1].append(topic_number)

        return topics_appearance
