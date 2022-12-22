import numpy as np
import os
import pandas as pd
from keras_preprocessing.text import Tokenizer
from sklearn.tree import DecisionTreeClassifier

from src.datamanager import tokenize

TOPICS = 1000
data_path = os.path.join('..', 'data')


def vectorize_sequences(sequences, dimension=TOPICS):
    results = np.zeros((len(sequences), dimension), dtype=float)
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0
    return results


def clean_cart():
    df_tr = pd.read_csv(os.path.join(data_path, 'fa_tokens_train_clean.csv'), sep='|', header=None,
                        names=['review', 'score'])
    df_vl = pd.read_csv(os.path.join(data_path, 'fa_tokens_test_clean.csv'), sep='|', header=None,
                        names=['review', 'score'])
    df_ts = pd.read_csv(os.path.join(data_path, 'fa_tokens_validation_clean.csv'), sep='|', header=None,
                        names=['review', 'score'])

    tokens_tr = tokenize(df_tr, clean=False, stem=False, dataset='train_clean')
    tokens_vl = tokenize(df_vl, clean=False, stem=False, dataset='validation_clean')
    tokens_ts = tokenize(df_ts, clean=False, stem=False, dataset='test_clean')

    return cart(tokens_tr, tokens_vl, tokens_ts)


def simple_cart():
    df_tr = pd.read_csv(os.path.join(data_path, 'fa_tokens_train.csv'), sep='|', header=None,
                        names=['review', 'score'])
    df_vl = pd.read_csv(os.path.join(data_path, 'fa_tokens_test.csv'), sep='|', header=None,
                        names=['review', 'score'])
    df_ts = pd.read_csv(os.path.join(data_path, 'fa_tokens_validation.csv'), sep='|', header=None,
                        names=['review', 'score'])

    tokens_tr = tokenize(df_tr, clean=False, stem=False, dataset='train')
    tokens_vl = tokenize(df_vl, clean=False, stem=False, dataset='validation')
    tokens_ts = tokenize(df_ts, clean=False, stem=False, dataset='test')

    return cart(tokens_tr, tokens_vl, tokens_ts)


def stem_cart():
    df_tr = pd.read_csv(os.path.join(data_path, 'fa_tokens_train_stem.csv'), sep='|', header=None,
                        names=['review', 'score'])
    df_vl = pd.read_csv(os.path.join(data_path, 'fa_tokens_test_stem.csv'), sep='|', header=None,
                        names=['review', 'score'])
    df_ts = pd.read_csv(os.path.join(data_path, 'fa_tokens_validation_stem.csv'), sep='|', header=None,
                        names=['review', 'score'])

    tokens_tr = tokenize(df_tr, clean=False, stem=False, dataset='train_stem')
    tokens_vl = tokenize(df_vl, clean=False, stem=False, dataset='validation_stem')
    tokens_ts = tokenize(df_ts, clean=False, stem=False, dataset='test_stem')

    return cart(tokens_tr, tokens_vl, tokens_ts)


def cart(tokens_tr, tokens_vl, tokens_ts):
    x_tr = tokens_tr['review'].values
    x_vl = tokens_vl['review'].values
    x_ts = tokens_ts['review'].values
    y_tr = tokens_tr['score'].values
    y_vl = tokens_vl['score'].values
    y_ts = tokens_ts['score'].values

    tokenizer = Tokenizer(num_words=TOPICS)
    tokenizer.fit_on_texts(x_tr)

    x_tr = tokenizer.texts_to_sequences(x_tr)
    x_vl = tokenizer.texts_to_sequences(x_vl)
    x_ts = tokenizer.texts_to_sequences(x_ts)

    x_tr = vectorize_sequences(x_tr, dimension=TOPICS)
    x_vl = vectorize_sequences(x_vl, dimension=TOPICS)
    x_ts = vectorize_sequences(x_ts, dimension=TOPICS)

    x_tr = np.concatenate((x_tr, x_vl, x_ts))
    y_tr = np.concatenate((y_tr, y_vl, y_ts))

    model = DecisionTreeClassifier()
    model.fit(x_tr, y_tr)

    keys = list(tokenizer.index_word.values())
    values = [topic_weight for k, topic_weight in enumerate(model.feature_importances_[1:TOPICS])]
    topic_weights = dict(zip(keys, values))
    return topic_weights
