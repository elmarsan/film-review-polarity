import numpy as np
from keras_preprocessing.text import Tokenizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot

from datamanager import load_datasets, tokenize
from plots import wordcloud_cart_plot
from sklearn.preprocessing import scale

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
# x_vl = tokenizer.texts_to_sequences(x_vl)
# x_ts = tokenizer.texts_to_sequences(x_ts)

# score: negative = [1 - 5], positive [6 - 10]
y_tr[y_tr <= 5] = 0
y_tr[y_tr > 5] = 1

def vectorize_sequences(sequences, dimension=1000):
    results = np.zeros((len(sequences), dimension), dtype=float)
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0
    return results


x_tr = vectorize_sequences(x_tr, dimension=TOPICS)
# x_vl = vectorize_sequences(x_vl, dimension=TOPICS)
# x_ts = vectorize_sequences(x_ts, dimension=TOPICS)

# model = DecisionTreeClassifier()
model = RandomForestClassifier()
# fit the model
model.fit(x_tr, y_tr)
# get importance
importance = model.feature_importances_
important_word_idxs = np.flip(np.argsort(importance))
# summarize feature importance
weights = {}
for i in range(100):
    idx = important_word_idxs[i]
    weights[tokenizer.index_word[idx]] = importance[idx]
    print(f'{i + 1:3d} word: : {tokenizer.index_word[idx]:20s} importance: {importance[idx]:.5f}')

wordcloud_cart_plot(weights)


def class_feature_importance(x, y, feature_importances):
    n, m = x.shape
    x = scale(x)

    out = {}
    for c in set(y):
        out[c] = np.mean(x[y == c, :], axis=0) * feature_importances

    return out


importance_per_class = class_feature_importance(x_tr, y_tr, importance)
importance_bad, importance_good = importance_per_class[0], importance_per_class[1]
important_word_bad_idxs = np.flip(np.argsort(importance_bad))
important_word_good_idxs = np.flip(np.argsort(importance_good))

weights_bad = {}
weights_good = {}
for i in range(100):
    idx_bad = important_word_bad_idxs[i]
    idx_good = important_word_good_idxs[i]
    weights_bad[tokenizer.index_word[idx_bad]] = importance_bad[idx_bad]
    weights_good[tokenizer.index_word[idx_good]] = importance_good[idx_good]
    print(f'{i + 1:3d} G word: : {tokenizer.index_word[idx_good]:20s} importance: {importance_good[idx_good]:.5f}')
    print(f'{i + 1:3d} B word: : {tokenizer.index_word[idx_bad]:20s} importance: {importance_bad[idx_bad]:.5f}')

wordcloud_cart_plot(weights_bad)
wordcloud_cart_plot(weights_good)

