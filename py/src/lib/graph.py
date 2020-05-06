import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from wordcloud import WordCloud
from PIL import Image
from os import path
import os
import math

from sklearn.cluster import AgglomerativeClustering

class graph:
    def __init__(self):
        self.fig_path = './figures/'

    def plot_cloud(self, text, title):
        plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

        plt.clf()
        wordcloud = WordCloud().generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        # plt.show()
        plt.savefig(self.fig_path + title + '.png')    
    def plot_barh(self, columns,counts, title, x_label,y_label):
        plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
        plt.clf()
        plt.barh(columns,counts)
        for i, v in enumerate(counts):
            plt.text(v, i, str(v), color='blue', fontweight='bold')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        # plt.show()
        plt.savefig(fig_path + title + '.png')
        

    def plot_heat(self, columns,counts, title, x_label,y_label):
        plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

        plt.clf()
        df = pd.DataFrame(counts,
                        columns=columns) 
        ax = sns.heatmap(df)
        # plt.show()
        plt.savefig(self.fig_path + title + '.png')  

    def dendro(dist, title,linkage='single', truncate_mode=None, metric = 'cosine'):
        linkage_matrix = sch.linkage(dist, method=linkage, metric=metric, optimal_ordering=False)
        print('linkage_matrix', linkage_matrix.shape)
        print('linkage_matrix', linkage_matrix[0:5])
        dist_1d = linkage_matrix.ravel()
        print('min-max', min(dist_1d),max(dist_1d))    
        fig, ax = plt.subplots(figsize=(10, 6)) # set size
        ax = dendrogram(linkage_matrix)
        plt.title("Dendrograms of Ward Cluster") 
        method = linkage 
        plt.title('Hierarchical Clustering Dendrogram (method = %s)'%method)
        plt.xlabel('tf-idf vector index')
        plt.ylabel('distance')

        plt.tight_layout() #show plot with tight layout
        plt.savefig(fig_path + 'clusters_'+title+'_'+linkage + '.png', dpi=200) #save figure as ward_clusters
        plt.close()

