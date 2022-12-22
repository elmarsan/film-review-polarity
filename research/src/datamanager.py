import os
import sys
import string
import pickle
import unidecode
import numpy as np
import pandas as pd
from multiprocessing import Pool

from nltk import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import cess_esp as cess
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from country_list import countries_for_language
from fuzzywuzzy import fuzz

data_path = os.path.join('..', 'data')


def build_datasets():
    print('Loading reviews...')
    df = load_raw_data()
    print('Creating trainining, validation and test datasets...')
    df_tr, df_ts, y_tr, y_ts = train_test_split(df, df[['score']],
                                                test_size=0.50, stratify=df[['score']], random_state=42)
    df_vl, df_ts, y_vl, y_ts = train_test_split(df_ts, y_ts, test_size=0.50, stratify=df_ts[['score']],
                                                random_state=42)
    print('Saving trainining, validation and test datasets...')
    df_tr.to_csv(os.path.join(data_path, 'fa_train.csv'), index=False, header=True, sep='|')
    df_ts.to_csv(os.path.join(data_path, 'fa_test.csv'), index=False, header=True, sep='|')
    df_vl.to_csv(os.path.join(data_path, 'fa_validation.csv'), index=False, header=True, sep='|')


def load_raw_data():
    filename = os.path.join(data_path, 'filmaffinity_reviews_150437_.txt')
    df = pd.read_csv(filename, sep='|', header=None, names=['film_id', 'user', 'date', 'city_country',
                                                            'review_title', 'review', 'unknown', 'score',
                                                            'percent'])
    countries = dict(countries_for_language('es'))

    def find_country_key(x):
        country_name = x['city_country'][x['city_country'].find('(') + 1:x['city_country'].find(')')]
        best_ratio = 0
        best_key = '??'
        for key, name in countries.items():
            ratio = fuzz.ratio(country_name.lower(), name.lower())
            if ratio == 100:
                return key
            elif ratio > best_ratio:
                best_ratio = ratio
                best_key = key
        if best_ratio > 90:
            return best_key

    tqdm.pandas(file=sys.stdout, leave=False)
    df['country'] = df.progress_apply(find_country_key, axis=1)
    df['city'] = df.apply(lambda x: x['city_country'][:x['city_country'].find('(') - 1], axis=1)
    df = df.drop(columns=['film_id', 'user', 'date', 'city_country', 'unknown', 'percent'])
    df = df.loc[df['review'].str.len() > 2]

    return df


def load_datasets():
    if not os.path.isfile(os.path.join(data_path, 'fa_train.csv')) or \
            not os.path.isfile(os.path.join(data_path, 'fa_validation.csv')) or \
            not os.path.isfile(os.path.join(data_path, 'fa_test.csv')):
        build_datasets()
    df_tr = pd.read_csv(os.path.join(data_path, 'fa_train.csv'), sep='|')
    df_vl = pd.read_csv(os.path.join(data_path, 'fa_validation.csv'), sep='|')
    df_ts = pd.read_csv(os.path.join(data_path, 'fa_test.csv'), sep='|')

    return df_tr, df_vl, df_ts


def tokenize_dataframe(dataframe, clean=True, stem=False):
    if stem:
        stemmer = SnowballStemmer('spanish')
    else:
        stemmer = None
    dataframe['review'] = dataframe['review'].apply(tokenize_sentence, args=[clean, stemmer])
    return dataframe


def tokenize_sentence(sentence, clean=True, stemmer=None):
    stop_words = set(stopwords.words('spanish'))
    string_text = sentence.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).lower()
    words = word_tokenize(string_text, language='spanish')
    words_filtered = [unidecode.unidecode(w) for w in words if w not in stop_words]
    if clean:
        words_es = set(cess.words())
        words_filtered = [w for w in words_filtered if w.lower() in words_es and len(w) > 1]
    if stemmer is not None:
        words_filtered = [stemmer.stem(w) for w in words_filtered]
    return ' '.join(words_filtered)


def tokenize(df, clean, stem, dataset, build=False):
    filename = os.path.join(data_path, f'fa_tokens_{dataset}{"_clean" if clean else ""}{"_stem" if stem else ""}.csv')
    if os.path.isfile(filename) and not build:
        df_result = pd.read_csv(filename, sep='|')
    else:
        df_split = np.array_split(df, 10)
        pool = Pool(10)
        df_result = pd.concat(pool.starmap(tokenize_dataframe, zip(df_split, [clean]*10, [stem]*10)))
        pool.close()
        pool.join()
        df_result = df_result[['review', 'score']]
        df_result.to_csv(filename, index=False, header=True, sep='|')
    return df_result
