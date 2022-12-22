import os
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from wordcloud import WordCloud

from src.datamanager import load_datasets
from src.cart import simple_cart, stem_cart, clean_cart

data_path = os.path.join('..', 'data')


def violinplot_nwords():
    print('Loading datasets...')
    df_tr, df_va, df_ts = load_datasets()
    df_tr['set'] = 'training'
    df_va['set'] = 'validation'
    df_ts['set'] = 'test'

    data = pd.concat([df_tr, df_va, df_ts], axis=0, ignore_index=True)
    data['count'] = data.apply(lambda x: len(x['review'].split(' ')), axis=1)
    data['rating'] = 'positive'
    data.loc[data['score'] <= 5, 'rating'] = 'negative'

    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=200)
    colors = sns.color_palette('pink', 10)[2], sns.color_palette('pink', 10)[4]
    ax = sns.violinplot(x='set', y='count', hue='rating', data=data,
                        palette=colors, split=True)
    ax.set_ylim([0, 1400])
    plt.xlabel('dataset')
    plt.ylabel('word count')
    plt.show()


def choropleth_nreviews():
    print('Loading datasets...')
    df_tr, df_va, df_ts = load_datasets()
    data = pd.concat([df_tr, df_va, df_ts], axis=0, ignore_index=True)
    shapefile = os.path.join(data_path, 'countries', 'ne_110m_admin_0_countries.shp')
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ISO_A2', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    gdf = gdf.loc[gdf['country'] != 'Antarctica']

    counts = data['country'].value_counts().to_frame().reset_index().rename({'index': 'code', 'country': 'count'},
                                                                            axis=1)
    merged = gdf.merge(counts, how='left', left_on='country_code', right_on='code').drop(['code'], axis=1)
    vmin, vmax = min(counts['count']), max(counts['count'])
    merged['count'] = (np.log10(merged['count']) + 1).fillna(0)
    fig, ax = plt.subplots(1, figsize=(10, 4.5), dpi=200)
    cmap = 'pink_r'
    merged.plot(column='count', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=matplotlib.colors.LogNorm(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm, fraction=0.021, pad=0.04)
    cbar.ax.set_yticklabels([f'{int(x)}' for x in [10 ** v for v in range(6)]], fontsize=11)

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax.axis('tight')
    ax.axis('off')
    plt.show()


def barchart_scores():
    print('Loading datasets...')
    dfs = load_datasets()
    scores = np.zeros((10, 3), dtype=float)
    for score in range(1, 11):
        for i, df in enumerate(dfs):
            scores[score - 1, i] = df.loc[df['score'] == score].shape[0]
    for i in range(3):
        scores[:, i] = 100 * scores[:, i] / np.sum(scores[:, i])

    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]

    x = np.arange(1, 11)
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots(1, figsize=(10, 7), dpi=200)
    cmap = cm.get_cmap('pink', 10)
    rects_tr = ax.bar(x - width, scores[:, 0], width, label='Training', color=cmap(2))
    rects_va = ax.bar(x, scores[:, 1], width, label='Validation', color=cmap(4))
    rects_ts = ax.bar(x + width, scores[:, 2], width, label='Test', color=cmap(5))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('%')
    ax.set_xlabel('score')
    ax.set_title('Review scores percentage by dataset')
    ax.set_xticks(x)
    ax.legend()
    fig.tight_layout()
    plt.show()


def wordcloud_cart_plot(weights):
    wc = WordCloud(background_color="white", width=2000, height=1200, relative_scaling=0.6,
                   normalize_plurals=False, colormap='pink_r').generate_from_frequencies(weights)
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.show()


if __name__ == '__main__':
    violinplot_nwords()
    choropleth_nreviews()
    barchart_scores()
    wordcloud_cart_plot(simple_cart())
    wordcloud_cart_plot(stem_cart())
    # wordcloud_cart_plot(clean_cart())
