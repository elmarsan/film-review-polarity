import os
import sys
import numpy as np
from tqdm import tqdm
from datamanager import data_path

embeddings_index = {}
with open(os.path.join(data_path, 'word_embeddings', 'SBW-vectors-300-min5.txt')) as f:
    line = f.readline().split()
    n = int(line[0])
    emb_dim = int(line[1])
    print(f'{n} word vectors. Embedding dimmension: {emb_dim}')
    for line in tqdm(f, total=n, file=sys.stdout, leave=False):
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs

embedding_matrix = np.zeros((n, emb_dim))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector


