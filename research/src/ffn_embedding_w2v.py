import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import sys
import numpy as np
from tqdm import tqdm
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from tensorflow.keras import layers, models, optimizers
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Embedding, Flatten

from datamanager import load_datasets, tokenize, data_path

if __name__ == '__main__':
    print('Loading datasets...')
    df_tr, df_vl, df_ts = load_datasets()
    clean = False
    stem = False
    print(f'stemming: {stem}, cleaning: {clean}')
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

    TOPICS = 5000
    tokenizer = Tokenizer(num_words=TOPICS)
    tokenizer.fit_on_texts(x_tr)
    tokens_dict = tokenizer.word_index
    x_tr = tokenizer.texts_to_sequences(x_tr)
    x_vl = tokenizer.texts_to_sequences(x_vl)
    x_ts = tokenizer.texts_to_sequences(x_ts)

    embeddings_index = {}
    # with open(os.path.join(data_path, 'word_embeddings', 'SBW-vectors-300-min5.txt')) as f:
    with open(os.path.join(data_path, 'word_embeddings', 'glove-sbwc.i25.vec')) as f:
        line = f.readline().split()
        n = int(line[0])
        emb_dim = int(line[1])
        print(f'{n} word vectors. Embedding dimmension: {emb_dim}')
        for line in tqdm(f, total=n, file=sys.stdout, leave=False):
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    embedding_matrix = np.zeros((len(tokens_dict) + 1, emb_dim))
    for word, i in tokens_dict.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    # score: negative = [1 - 5], positive [6 - 10]
    y_tr[y_tr <= 5] = 0
    y_tr[y_tr > 5] = 1
    y_vl[y_vl <= 5] = 0
    y_vl[y_vl > 5] = 1
    y_ts[y_ts <= 5] = 0
    y_ts[y_ts > 5] = 1

    dropout = 0.15
    epochs = 10
    num_neurons = 256
    maxlen = 256
    batch_size = 128

    x_tr = pad_sequences(x_tr, padding='post', maxlen=maxlen)
    x_vl = pad_sequences(x_vl, padding='post', maxlen=maxlen)
    x_ts = pad_sequences(x_ts, padding='post', maxlen=maxlen)

    model = models.Sequential()
    embedding_layer = Embedding(input_dim=len(tokens_dict) + 1, output_dim=emb_dim, weights=[embedding_matrix],
                                input_length=maxlen, trainable=False)
    model.add(embedding_layer)
    model.add(Flatten())
    model.add(layers.Dense(num_neurons, activation='relu', input_shape=(TOPICS,)))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(num_neurons, activation='relu'))
    model.add(layers.Dropout(dropout))
    model.add(layers.Dense(1, activation='sigmoid'))

    # optimizer = optimizers.Adam(learning_rate=0.001)
    optimizer = optimizers.RMSprop(learning_rate=0.001)

    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])
    es = EarlyStopping(monitor='val_loss', patience=3)
    history = model.fit(x_tr, y_tr, batch_size=batch_size, epochs=epochs, validation_data=(x_vl, y_vl), callbacks=es)

    evaluation = model.evaluate(x_ts, y_ts)
    print(evaluation)
