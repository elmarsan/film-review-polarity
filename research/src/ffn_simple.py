from keras_preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras import layers, models, optimizers
from tensorflow.python.keras.callbacks import EarlyStopping
from datamanager import load_datasets, tokenize

if __name__ == '__main__':
    print('Loading datasets...')
    df_tr, df_vl, df_ts = load_datasets()
    clean = False
    stem = True
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

    TOPICS = 10000
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

    drop_layers = 0.5
    epochs = 10
    num_neurons = 256
    batch_size = 128

    model = models.Sequential()

    model.add(layers.Dense(num_neurons, activation='relu', input_shape=(TOPICS,)))
    model.add(layers.Dropout(drop_layers))
    model.add(layers.Dense(num_neurons, activation='relu'))
    model.add(layers.Dropout(drop_layers))
    model.add(layers.Dense(1, activation='sigmoid'))

    optimizer = optimizers.RMSprop(learning_rate=0.001)

    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])
    es = EarlyStopping(monitor='val_loss', patience=3)
    history = model.fit(x_tr, y_tr, batch_size=batch_size, epochs=epochs, validation_data=(x_vl, y_vl), callbacks=es)

    evaluation = model.evaluate(x_ts, y_ts)
    print(evaluation)

    # [0.5752211213111877, 0.8274927139282227] 2048
    # [0.5700678825378418, 0.8334751129150391] 1024
    # [0.4122689962387085, 0.8353097438812256] 256
