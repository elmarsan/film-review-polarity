import sys
import numpy as np
from tqdm import tqdm


class NaiveBayes:

    def __init__(self):
        self.vocabulary = None

    def fit(self, x, y, length):
        v = {'0': {}, '1': {}, 'words': {}, 'r': {}, 'rt': 0}
        pw_count = 0
        nw_count = 0
        pr_count = 0
        nr_count = 0
        unique = set()
        for i in tqdm(range(x.shape[0]), file=sys.stdout, leave=False):
            tokens = x[i]
            pos = y[i] > 0
            pr_count += int(pos)
            nr_count += int(not pos)
            if pos:
                pw_count += len(tokens)
            else:
                nw_count += len(tokens)
            for token in tokens:
                unique.add(token)
                v['1'][token] = v['1'].get(token, 0) + int(pos)
                v['0'][token] = v['0'].get(token, 0) + int(not pos)

        unique = list(unique)
        if length is not None and len(unique) > length:
            diffs = []
            for token in unique:
                diffs.append(abs(v['1'][token] - v['0'][token]))
            unique = [unique[w_idx] for w_idx in np.argsort(diffs)[:length]]
            vp = {w: v['1'][w] for w in unique}
            vn = {w: v['0'][w] for w in unique}
            v['1'] = vp
            v['0'] = vn

        n_unique = len(unique)
        v['words'] = unique
        v['rt'] = pr_count / nr_count

        # Laplacian smoothing
        for word in unique:
            v['1'][word] = (v['1'][word] + 1) / (pw_count + n_unique)
            v['0'][word] = (v['0'][word] + 1) / (nw_count + n_unique)
            v['r'][word] = v['1'][word] / v['0'][word]

        self.vocabulary = v

    def predict(self, tokens):
        y_hat = np.zeros(tokens.shape[0])
        log_prior = np.log10(self.vocabulary['rt'])
        for i, tokens in tqdm(enumerate(tokens), file=sys.stdout, leave=False, total=tokens.shape[0]):
            log_l = 0
            for word in tokens:
                value = self.vocabulary['r'].get(word, 1)
                log_l += np.log10(value)
            y_hat[i] = 1 if log_l > 0 else 0

        return y_hat
