import itertools
from datamanager import build_datasets, load_datasets, tokenize

build_datasets()
print('Loading datasets...')
df_tr, df_vl, df_ts = load_datasets()

for clean, stem in itertools.product([False, True], [False, True]):
    print(f'stemming: {stem}, cleaning: {clean}')
    print('Tokenizing train data...')
    tokens_tr = tokenize(df_tr, clean=clean, stem=stem, dataset='train', build=True)
    print('Tokenizing validation data...')
    tokens_vl = tokenize(df_vl, clean=clean, stem=stem, dataset='validation', build=True)
    print('Tokenizing test data...')
    tokens_ts = tokenize(df_ts, clean=clean, stem=stem, dataset='test', build=True)
