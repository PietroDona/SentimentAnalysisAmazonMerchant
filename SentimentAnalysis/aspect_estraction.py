from SentimentAnalysis.aspect_data_structure import Aspect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy

import pandas as pd


nlp = spacy.load('en_core_web_md', exclude="ner")
senticnet = pd.read_csv("SentimentAnalysis/senticnet.csv")
sia = SentimentIntensityAnalyzer()


def senticnet_search(query):
    '''Search if {query} list of word is present in the senticnet list'''
    processed_query = ("_".join(query)).lower()
    return not senticnet[senticnet["Aspect"] == processed_query].empty


def rule1(doc):
    '''
    Aspect extraction following Subject Noun Rule 1
    There is a subject of t that has any adverbial or adjective modifier.
    T is the aspect
    '''
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:
            for child in token.head.children:
                if child.dep_ in ["amod", "advmod"] and not token.head.is_stop:
                    if senticnet_search([token.head.lemma_]):
                        return Aspect(aspect=token.head.lemma_, rule=1)


def rule2(doc):
    '''
    Aspect extraction following Subject Noun Rule 2
    Sentence without auxiliary verbs and t with adjective, adverbial or adverbial modifier clause with another token -> h and t are aspects
    or with direct object relation with a NOUN n, n is aspect if in SentiNet
    or with direct object relation with a NOUN n and not in SentiNet derive list of connected nouns and that is aspect
    or open clausal complement with another token
    '''
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:
            # check if an AUX is present
            aux_presence = [t for t in doc if t.pos_ == "AUX"]
            for child in token.head.children:
                if child.dep_ in ["amod", "advmod", "advcl"] and not aux_presence and not token.is_stop:
                    return Aspect(aspect=token.lemma_, rule=2)
                if child.dep_ == "dobj" and child.pos_ == "NOUN" and not aux_presence and not child.is_stop:
                    if senticnet_search([child.lemma_]):
                        return Aspect(aspect=child.lemma_, rule=2)
                    else:
                        tmp = " ".join([child.lemma_]+[cococ.lemma_ for coc in child.children if coc.pos_ ==
                                                       "ADP" for cococ in coc.children if cococ.pos_ == "NOUN"])
                        return Aspect(aspect=tmp,  rule=2)

                if child.dep_ == "xcomp" and not child.is_stop:
                    # if [child,coc] is in SenticNet
                    tmp = [[child.lemma_, coc.lemma_]
                           for coc in child.children]
                    for coc in child.children:
                        if senticnet_search([child.lemma_, coc.lemma_]) or senticnet_search([coc.lemma_, child.lemma_]):
                            return Aspect(aspect=" ".join([child.lemma_, coc.lemma_]), rule=2)
                    else:
                        tmp = [
                            cococ.lemma_ for coc in child.children for cococ in coc.children if cococ.pos_ == "NOUN"]
                        if tmp:
                            return Aspect(aspect=" ".join(tmp), rule=2)


def rule3(doc):
    '''
    Subject Noun Rule
    Sentence with auxiliary verb (copula) and token as complement -> token is aspect
    '''
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:
            for child in token.head.children:
                if child.dep_ in ["acomp"] and token.head.pos_ == "AUX" and not child.is_stop:
                    # check if child exists in the implicit aspect lexicon
                    # print(child)
                    return Aspect(aspect=child.lemma_, rule=3)


def rule4(doc):
    '''
    Subject Noun Rule
    Sentence with auxiliary verb (copula) and token as complement and a Noun -> noun is aspect
    '''
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:
            for child in token.head.children:
                if child.dep_ in ["acomp"] and token.head.pos_ == "AUX" and token.pos_ == "NOUN" and not token.is_stop:
                    return Aspect(aspect=token.lemma_, rule=4)


def rule5(doc):
    '''
    Subject Noun Rule
    Sentence with auxiliary verb (copula) and token as complement and a Noun -> noun is aspect
    '''
    for token in doc:
        if token.dep_ in ["nsubj", "nsubjpass"]:
            for child in token.head.children:
                if child.dep_ in ["acomp"] and token.head.pos_ == "AUX" and not child.is_stop:
                    # check if  child and coc exists in the implicit aspect lexicon
                    tmp = " ".join(
                        [child.lemma_]+[coc.lemma_ for coc in child.children if coc.pos_ == "VERB"])
                    return Aspect(aspect=tmp, rule=5)


def rule6(doc):
    '''
    NO Subject Noun Rule
    Sentence with adjective or adverb h in infinitival or open clausal complement -> if h in IAC lexicon -> h aspect
    '''
    for token in doc:
        if token.pos_ in ["ADJ", "ADV"]:
            for child in token.children:
                if child.dep_ in ["ccomp", "xcomp"] and not token.is_stop:
                    # if token is in IAC lexicon
                    return Aspect(aspect=token.lemma_, rule=6)


def rule7(doc):
    '''
    NO Subject Noun Rule
    h token connected to noun t through preposition -> h+t aspect
    '''
    for token in doc:
        for child in token.children:
            if child.dep_ == "prep":
                for child_of_child in child.children:
                    if child_of_child.pos_ == "NOUN" and not token.is_stop:
                        return Aspect(aspect=f"{token.lemma_} {child_of_child.lemma_}", rule=4)


def rule8(doc):
    '''
    NO Subject Noun Rule
    h token connected with direct object with t -> t aspect
    '''
    for token in doc:
        for child in token.children:
            if child.dep_ == "dobj" and not child.is_stop:
                return Aspect(aspect=child.lemma_, rule=8)


def extract_aspect_sentence(doc):
    '''Extract the aspects from a sentence'''
    SubjectRule = {"rule1": rule1, "rule2": rule2, "rule3": rule3,
                   "rule4": rule4, "rule5": rule5}
    NoSubjectRule = {"rule6": rule6, "rule7": rule7, "rule8": rule8}
    subjects = [token for token in doc if token.dep_ in ["nsubj", "nsubjpass"]]
    aspects = []
    if subjects:
        for name, rule in SubjectRule.items():
            if a := rule(doc):
                if a not in aspects:
                    a.sentiment = sia.polarity_scores(doc.text).get('compound')
                    aspects.append(a)

    else:
        for name, rule in NoSubjectRule.items():
            if a := rule(doc):
                if a not in aspects:
                    a.sentiment = sia.polarity_scores(doc.text).get('compound')
                    aspects.append(a)
    return aspects


def get_aspects(text: str):
    doc = nlp(text)
    aspects = []
    for sent in doc.sents:
        tmp_aspects = extract_aspect_sentence(sent)
        aspects += tmp_aspects
    return aspects
