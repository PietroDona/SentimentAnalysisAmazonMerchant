# Analyze Amazon.com Product Reviews

This package extracts aspects (or product features) from the content of the reviews and infers the associated polarity. Consider, for example, the review of a candle

`**Smells** yummy but started to **burn unevenly** halfway thru (couldn't keep it lit anymore). But **gorgeous** for gifting!!`

The review consists of three aspects with three different opinions. The smell and the manufacture of the product are rated very positively. However, there is a problem with the burning of the candle. The overall rating is 4/5.

The code is a python implementation of
[A Rule-Based Approach to Aspect Extraction from Product Reviews.
Poria, Soujanya & Cambria, Erik & Ku, Lun-Wei & Gui, Chen & Gelbukh, Alexander.
SocialNLP. 2014. 10.3115/v1/W14-5905.](literature/A_Rule-Based_Approach_to_Aspect_Extraction_from_Product_Reviews.pdf)

The division in sentences of the reviews and the part of speech (POS) and dependences (DEP) are done using the NLP library [spacy](https://spacy.io). The eight semantic rules suggested in the literature are implemented in python. Please read [this notebook](notebooks/AspectExtraction.ipynb) for a more in-depth analysis and test.

A polarity score is associated with each aspect by applying `nltk` VADER SentimentIntensityAnalyzer to the parent sentence.

To interpret the aspect extraction procedure on thousands of reviews is necessary to group them by meaning. We use KMeans clustering analysis applied to the vectorial representation of the aspects to group them automatically. For example, among the reviews of a candle, the following aspects are extracted.

-   scent
-   fragrance
-   aroma
-   smell

They are referring to the same feature of the product: the smell. It makes sense to consider them as one single group from the point of view of product analysis. KMeans is the most straightforward option at our disposal but is performing surprisingly well.
