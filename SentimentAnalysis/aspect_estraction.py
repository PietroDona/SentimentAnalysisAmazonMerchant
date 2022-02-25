from dataclasses import dataclass


@dataclass
class Aspect:
    aspect: str
    modifier: str
    rule: int

    def __post_init__(self):
        self.aspect = self.aspect.lower()
        self.modifier = self.modifier.lower()

    def __repr__(self):
        return f"<Aspect - {self.aspect} | Modifier - {self.modifier} | Rule {self.rule}>"

    def __str__(self):
        return self.__repr__()


def rule1(doc):
    '''
        Rule 1 of Aspect extraction (M = Modifier , A = Aspect)
        # Adjectival modifier - https://universaldependencies.org/docs/en/dep/amod.html
         - M is a amod but not a STOPWORD
         - A is its head.

        EXAMPLE
        "These are not very amazing headphones"
        ('very not amazing', 'headphones')
    '''
    for token in doc:
        M = None
        A = None
        if token.dep_ == "amod" and not token.is_stop:
            M = token.text
            A = token.head.text

            # We add all possible adverbial modifier that
            # change the strength of the modifier
            # (advmod - https://universaldependencies.org/docs/en/dep/advmod.html)
            # and negations of the amod
            for child_m in token.children:
                if(child_m.dep_ == "neg"):
                    M = f"not {M}"

                if(child_m.dep_ == "advmod"):
                    M = f"{child_m.text} {M}"
        if M and A:
            return Aspect(modifier=M, aspect=A, rule=1)
    return None


def rule2(doc):
    '''
        Rule 2 of Aspect extraction (M = Modifier , A = Aspect)
        Direct Object - http://universaldependencies.org/docs/en/dep/dobj.html
         - Token (usually VERB representing an action)
         - M is a child with relationship of dobj (accusative object)
         - A is a child with relationship of nsubj (nominal subject)
        Assumption - A verb will have only one NSUBJ and DOBJ


    '''
    for token in doc:
        M = None
        A = None
        neg_prefix = None
        for child in token.children:
            if child.dep_ == "nsubj" and not child.is_stop:
                A = child.text

            if child.dep_ == "dobj" and not child.is_stop:
                M = child.text
                for child_of_child in child.children:
                    if child_of_child.text.lower() in ["no", "not"]:
                        M = f"{child_of_child.text} {M}"

            # If amongs the childs we find a negation we add it to the modifier
            # This will not work in case of double negations/corner cases
            if child.dep_ == "neg":
                neg_prefix = child.text

        if (neg_prefix and M):
            M = f"{neg_prefix} {M}"
        if M and A:
            return Aspect(modifier=M, aspect=A, rule=2)
    return None


def rule3(doc):
    '''
        Rule 3 of Aspect extraction (M = Modifier , A = Aspect)
        Adjectival Complement
         - Token (usually VERB representing an action)
         - M is a child with relationship of acomp (adjectival complement)
         - A is a child with relationship of nsubj (nominal subject)
        EXAMPLE
        "These headphones are not amazing"
        ('amazing', 'headphones')
    '''
    for token in doc:
        M = None
        A = None
        neg_prefix = None
        for child in token.children:
            if child.dep_ == "nsubj" and not child.is_stop:
                A = child.text
            # Work around imperative sentences
            if child.head.dep_ == "ROOT" and not A:
                A = child.head.text
            if(child.dep_ == "acomp" and not child.is_stop):
                M = child.text

            # We need to keep the auxiliaries and negations
            # We ignore double negations
            if(child.dep_ == "aux" and child.tag_ == "MD") or (child.dep_ == "neg"):
                neg_prefix = "not"

        if (neg_prefix and M):
            M = f"{neg_prefix} {M}"

        if M and A:
            return Aspect(modifier=M, aspect=A, rule=3)
    return None


def rule4(doc):
    '''
        Rule 4 of Aspect extraction(M=Modifier, A=Aspect)
        Adverbial modifier to a passive verb
         - Token
            - M is a child with relationship of advmod (adverbial modifier)
            - A is a child with relationship of nsubjpass (passive nominal subject)
        EXAMPLE
        "These headphones work incredibly"
        ('incredibly', 'headphones')
    '''
    for token in doc:
        M = None
        A = None
        neg_prefix = None
        for child in token.children:
            if((child.dep_ == "nsubjpass" or child.dep_ == "nsubj") and not child.is_stop):
                A = child.text

            if(child.dep_ == "advmod" and not child.is_stop):
                M = child.lemma_
                # Add additional modifiers
                for child_m in child.children:
                    if(child_m.dep_ == "advmod"):
                        M = f"{child_m.text} M"
            # Add negations
            if child.dep_ == "neg":
                neg_prefix = "not"

        if (neg_prefix and M):
            M = f"{neg_prefix} {M}"

        if M and A:
            return Aspect(modifier=M, aspect=A, rule=4)
    return None


def rule5(doc):
    '''
        Rule 5 of Aspect extraction(M=Modifier, A=Aspect)
        Complement of a copular verb
        A copular verb is a special kind of verb used to join an adjective or noun complement to a subject.  
        Common examples are: be (is, am, are, was, were), appear, seem, look, sound, smell, taste, feel, become and get.
         - Token
            - M is a copular verb ?
            - A is a nsubj
    '''
    for token in doc:
        A = None
        M = None
        for child in token.children:
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
            if(child.dep_ == "cop" and not child.is_stop):
                M = child.text
        if M and A:
            return Aspect(modifier=M, aspect=A, rule=5)
    return None


def rule6(doc):
    '''
        Rule 6 of Aspect extraction(M=Modifier, A=Aspect)
        Interjection
        - M is an Interjection
        - A is its nsubj
    '''
    for token in doc:
        A = None
        M = None
        if(token.pos_ == "INTJ" and not token.is_stop):
            for child in token.children:
                if(child.dep_ == "nsubj" and not child.is_stop):
                    A = child.text
                    M = token.text
        if M and A:
            return Aspect(modifier=M, aspect=A, rule=6)
    return None


def rule7(doc):
    '''
        Rule 7 of Aspect extraction(M=Modifier, A=Aspect)
        Interjection
        - M is an Interjection
        - A is its nsubj
    '''
    for token in doc:
        M = None
        A = None
        neg_prefix = None
        for child in token.children:
            if child.dep_ == "nsubj" and not child.is_stop:
                A = child.text

            if child.dep_ == "attr" and not child.is_stop:
                M = child.text
            # Add negations
            if child.dep_ == "neg":
                neg_prefix = "not"

        if (neg_prefix and M):
            M = f"{neg_prefix} {M}"

        if M and A:
            return Aspect(modifier=M, aspect=A, rule=7)
    return None


def rule8(doc):
    '''
        Rule 8 of Aspect extraction(M=Modifier, A=Aspect)
        Adposition
        - M is an adjective in the head of the adposition
        - A is its obj
    '''
    for token in doc:
        M = None
        A = None
        if token.pos_ == "ADP":
            if token.head.pos_ == "ADJ":
                M = token.head.text
            for child in token.children:
                if child.dep_ == "pobj" and not child.is_stop:
                    A = child.text

        if M and A:
            return Aspect(modifier=M, aspect=A, rule=8)
    return None


rules = {"rule1": rule1, "rule2": rule2, "rule3": rule3,
         "rule4": rule4, "rule5": rule5, "rule6": rule6,
         "rule7": rule7, "rule8": rule8}
