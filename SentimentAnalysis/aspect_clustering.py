'''
Module to cluster the product review aspects
using KMeans algorithm. We choose 5 clusters conventionally
it will be improved with an automatic elbow analysis in a future update
'''

from sklearn.cluster import KMeans
import pandas as pd
from SentimentAnalysis import aspect_estraction
from pathlib import Path


def extract_aspects(dfproduct, strasin):
    aspects_pool = []
    ids = []

    for review, reviewID in zip(list(dfproduct["review_content"]), list(dfproduct.index)):
        tmp = aspect_estraction.get_aspects(review)
        aspects_pool += tmp
        ids += [reviewID]*len(tmp)

    aspects_words = [aspect_word.aspect for aspect_word in aspects_pool]
    words_polarity = [aspect_word.sentiment for aspect_word in aspects_pool]

    aspect_vectors = [aspect_estraction.nlp(
        aspect).vector for aspect in aspects_words]

    # Load all the reviews
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(aspect_vectors)
    labels = kmeans.labels_

    aspectsdf = pd.DataFrame(
        [z for z in zip(aspects_words, labels, words_polarity)], columns=["aspect", "cluster", "polarity"])
    aspectsdf.index = ids
    aspectsdfclustered = pd.merge(
        aspectsdf, dfproduct, left_index=True, right_index=True)

    testcluster = aspectsdfclustered.query("cluster==0").copy()
    cluster0 = testcluster['aspect'].value_counts().nlargest(4)

    testcluster = aspectsdfclustered.query("cluster==1").copy()
    cluster1 = testcluster['aspect'].value_counts().nlargest(4)

    testcluster = aspectsdfclustered.query("cluster==2").copy()
    cluster2 = testcluster['aspect'].value_counts().nlargest(4)

    testcluster = aspectsdfclustered.query("cluster==3").copy()
    cluster3 = testcluster['aspect'].value_counts().nlargest(4)

    testcluster = aspectsdfclustered.query("cluster==4").copy()
    cluster4 = testcluster['aspect'].value_counts().nlargest(4)

    clusterdf = pd.DataFrame({"Name0": cluster0.index,
                              "Count0": 100*cluster0.values / cluster0.values.sum(),
                              "Name1": cluster1.index,
                              "Count1": 100*cluster1.values / cluster1.values.sum(),
                              "Name2": cluster2.index,
                              "Count2": 100*cluster2.values / cluster2.values.sum(),
                              "Name3": cluster3.index,
                              "Count3": 100*cluster3.values / cluster3.values.sum(),
                              "Name4": cluster4.index,
                              "Count4": 100*cluster4.values / cluster4.values.sum()})
    product_path = Path("data") / strasin / "cluster_aspects_review.csv"
    clusterdf.to_csv(product_path, index=False)

    pospolarity = aspectsdfclustered.query(
        "polarity>0")["cluster"].value_counts()
    neupolarity = aspectsdfclustered.query(
        "polarity==0")["cluster"].value_counts()
    negpolarity = aspectsdfclustered.query(
        "polarity<0")["cluster"].value_counts()
    posrating = aspectsdfclustered.query("review_rating>3")[
        "cluster"].value_counts()
    neurating = aspectsdfclustered.query("review_rating==3")[
        "cluster"].value_counts()
    negrating = aspectsdfclustered.query("review_rating<3")[
        "cluster"].value_counts()

    clusternames = [cluster0.index[0], cluster1.index[0], cluster2.index[0],
                    cluster3.index[0], cluster4.index[0]]

    polaritycount = pd.DataFrame({
        "Cluster": pospolarity.index,
        "ClusterName": [clusternames[idx] for idx in pospolarity.index],
        "PositivePolarity": pospolarity.values,
        "NeutralPolarity": neupolarity.values,
        "NegativePolarity": negpolarity.values,
        "PositiveRating": posrating.values,
        "NeutralRating": neurating.values,
        "NegativeRating": negrating.values})

    product_path = Path("data") / strasin / "aspects_review_value.csv"
    polaritycount.to_csv(product_path, index=False)
