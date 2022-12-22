from sklearn.metrics import accuracy_score
from datamanager import load_datasets, tokenize
from models import NaiveBayes


if __name__ == '__main__':
    print('Loading datasets...')
    df_tr, df_vl, df_ts = load_datasets()
    clean = True
    stem = True
    print(f'stemming: {stem}, cleaning: {clean}')
    print('Tokenizing train data...')
    tokens_tr = tokenize(df_tr, clean=clean, stem=stem)
    # print('Tokenizing validation data...')
    # tokens_vl = tokenize(df_vl, clean=clean, stem=stem)
    print('Tokenizing test data...')
    tokens_ts = tokenize(df_ts, clean=clean, stem=stem)

    x_tr = tokens_tr['review'].values
    x_ts = tokens_ts['review'].values
    y_tr = tokens_tr['score'].values
    y_ts = tokens_ts['score'].values

    # score: negative = [1 - 5], positive [6 - 10]
    y_tr[y_tr <= 5] = 0
    y_tr[y_tr > 5] = 1
    y_ts[y_ts <= 5] = 0
    y_ts[y_ts > 5] = 1

    nb_model = NaiveBayes()
    print('Fitting Naïve Bayes model...')
    nb_model.fit(x_tr, y_tr, length=None)

    print('Predicting results...')
    y_hat = nb_model.predict(x_ts)
    acc = accuracy_score(y_ts, y_hat)
    # Naive Bayes: 0.78458  stem=False
    # Naive Bayes: 0.77227  stem=True
    print(f'accuracy: {acc:.5f}')
