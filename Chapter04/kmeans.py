import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns

from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE


# Set random seed for reproducibility
np.random.seed(1000)


min_nb_clusters = 2
max_nb_clusters = 20


if __name__ == '__main__':
    # Load the dataset
    digits = load_digits()
    X_train = digits['data'] / np.max(digits['data'])

    # Compute the inertias
    inertias = np.zeros(shape=(max_nb_clusters - min_nb_clusters + 1,))

    for i in range(min_nb_clusters, max_nb_clusters + 1):
        km = KMeans(n_clusters=i, random_state=1000)
        km.fit(X_train)
        inertias[i - min_nb_clusters] = km.inertia_

    # Plot the inertias
    sns.set()

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(np.arange(2, max_nb_clusters + 1), inertias, "o-")
    ax.set_xlabel("Number of clusters", fontsize=18)
    ax.set_ylabel("Inertia", fontsize=18)
    ax.set_xticks(np.arange(2, max_nb_clusters + 1))
    ax.grid(True)
    plt.show()

    # Perform K-Means with 10 clusters
    km = KMeans(n_clusters=10, random_state=1000)
    Y = km.fit_predict(X_train)

    # Show the centroids
    fig, ax = plt.subplots(1, 10, figsize=(10, 10))

    for i in range(10):
        c = km.cluster_centers_[i]
        ax[i].matshow(c.reshape(8, 8) * 255.0, cmap='gray')
        ax[i].set_xticks([])
        ax[i].set_yticks([])

    plt.show()

    # Perform t-SNE on the clustered dataset
    tsne = TSNE(n_components=2, perplexity=10.0, random_state=1000)
    X_tsne = tsne.fit_transform(X_train)

    fig, ax = plt.subplots(figsize=(20, 10))

    # Show the t-SNE clustered dataset
    for i in range(X_tsne.shape[0]):
        ax.scatter(X_tsne[i, 0], X_tsne[i, 1], marker='o', color=cm.Pastel1(Y[i]), s=450)
        if i % 10 == 0:
            ax.annotate('%d' % Y[i], xy=(X_tsne[i, 0], X_tsne[i, 1]), fontsize=18)

    ax.set_xlabel(r'$x_0$', fontsize=18)
    ax.set_ylabel(r'$x_1$', fontsize=18)

    for t in ax.xaxis.get_major_ticks():
        t.label.set_fontsize(16)

    for t in ax.yaxis.get_major_ticks():
        t.label.set_fontsize(16)

    ax.grid(True)

    plt.show()



