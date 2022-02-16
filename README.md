# SentimentAnalysisAmazonMerchant

Sentiment analysis aims at dentifying and categorize the sentiment in piece of text.

~~~~
It has a wide range of applications in industry from
forecasting market movements based on sentiment expressed in news and blogs, to identifying
customer satisfaction and dissatisfaction from their reviews and social media posts. It also forms
the basis for other applications like recommender systems.

Consumers can also assign a numerical value (i.e., rating) to the product
or service they are reviewing. On Amazon.com the rating can be between 1 and 5 where 1 is the
worst and 5 is the best. In some instances, there is a mismatch between a customer’s review and
rating. It is important to identify the reviews with mismatched ratings since individual ratings are
used to compute the average rating.


TRADITIONAL STRATEGY 
bag-of-words or
bag-of-n-grams + Classifier
1 loses ordering of words and
2 word order in short context but suffers of data sparsity and high dimensionality

Mikolov et al. also [4] introduced word vectors, which is an *unsupervised algorithm* to efficiently
capture semantics of words. Word vectors represent words as vectors and semantically similar
words are closer to each other in vector space
Interestingly, this
vector representation of text also captures linguistic patterns. For example, the result of vector
calculation vec("King") - vec("Queen") + vec("Woman") will output a vector that is closer to the
vector representation of word “Man" than to any other word. Their work was made available as an
open-source project titled word2vec and can be found on Google Code


In order to analyse the sentiment of Amazon.com reviews we built a model using recurrent neural
networks (RNN) with gated recurrent unit (GRU) that learned low-dimensional vector
representation of reviews using paragraph vectors and product embeddings.


1. Removing hyperlinks.
2. Removing unwanted spaces between words.
3. Converting informal words such as ‘I’ll’, ‘I’ve’ to its formal form ‘I will’, ‘I have’, etc.
4. Adding spaces between punctuation. For example, ‘This is great!It works.’ is converted to
‘This is great ! It works .’. Punctuations are treated as separate tokens to try to improve the
accuracy of the classifier.


Ratio of summary words to review text words
Number of sentences of each review text


*Review-centric features**

    Length of the review
    Average word length of the reviewer
    Number of sentences
    Average sentence length of the reviewer
    Percentage of numerals
    Percentage of capitalized words
    Percentage of positive/negative opinion bearing words in each review.

**Reviewer-centric features**

    Maximum number of reviews in a day
    Percentage of reviews with positive/negative ratings
    Average review length
    The standard deviation of ratings of the reviewer’s reviews

**Review-Text features**

I converted each review into a 100-element numerical representation (text vectors) using the Word2Vec, a pre-trained neural network model that learns vector representations of words.


# Setup

Create virtual environment and activate it
`python3 -m venv scraper-env`

`source scraper-env/bin/activate`

Install dependencies
`pip install -r requirements.txt`

Scrape the data
`python amazon_scrape.py`