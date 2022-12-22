from keras_preprocessing.text import Tokenizer
import numpy as np
from sklearn.decomposition import PCA
from tensorflow.keras import layers, models, optimizers
from tensorflow.python.keras.callbacks import EarlyStopping
from datamanager import load_datasets, tokenize

if __name__ == '__main__':
    print('Loading datasets...')
    df_tr, df_vl, df_ts = load_datasets()
    clean = False
    stem = False
    print(f'stemming: {stem}')
    print('Tokenizing train data...')
    tokens_tr = tokenize(df_tr, clean=clean, stem=stem, dataset='train')
    print('Tokenizing validation data...')
    tokens_vl = tokenize(df_vl, clean=clean, stem=stem, dataset='validation')
    print('Tokenizing test data...')
    tokens_ts = tokenize(df_ts, clean=clean, stem=stem, dataset='test')

    x_tr = tokens_tr['review'].values.tolist()
    x_vl = tokens_vl['review'].values.tolist()
    x_ts = tokens_ts['review'].values.tolist()
    y_tr = tokens_tr['score'].values
    y_vl = tokens_vl['score'].values
    y_ts = tokens_ts['score'].values

    TOPICS = 1000
    tokenizer = Tokenizer(num_words=TOPICS, lower=True)
    tokenizer.fit_on_texts(x_tr)
    x_tr = tokenizer.texts_to_sequences(x_tr)
    x_vl = tokenizer.texts_to_sequences(x_vl)
    x_ts = tokenizer.texts_to_sequences(x_ts)

    # score: negative = [1 - 5], positive [6 - 10]
    y_tr[y_tr <= 5] = 0
    y_tr[y_tr > 5] = 1
    y_vl[y_vl <= 5] = 0
    y_vl[y_vl > 5] = 1
    y_ts[y_ts <= 5] = 0
    y_ts[y_ts > 5] = 1


    def vectorize_sequences(sequences, dimension=1000):
        results = np.zeros((len(sequences), dimension), dtype=float)
        for i, sequence in enumerate(sequences):
            results[i, sequence] = 1.0
        return results

    x_tr = vectorize_sequences(x_tr, dimension=TOPICS)
    x_vl = vectorize_sequences(x_vl, dimension=TOPICS)
    x_ts = vectorize_sequences(x_ts, dimension=TOPICS)

    pca = PCA(n_components=100, svd_solver='arpack')
    pca.fit(x_tr, y_tr)
    x_tr = pca.transform(x_tr)