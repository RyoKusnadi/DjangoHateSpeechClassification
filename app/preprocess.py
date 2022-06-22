import pandas as pd
import nltk
from nltk.corpus import stopwords
import pickle

nltk.download('stopwords')


def find_features(document, word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features


def clean(message):
    words = [word for word in message.split() if not word.startswith('@')]
    stop_words = set(stopwords.words('indonesian'))
    filtered_sentence = [w.split('.')[0].lower() for w in words if not w in stop_words]

    word_features = pd.read_csv('app/features.csv').values[0][1:].tolist()

    featureset=find_features(filtered_sentence,word_features)

    return featureset
