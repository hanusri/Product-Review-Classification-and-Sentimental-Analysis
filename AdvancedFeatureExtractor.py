from nltk.tokenize.regexp import RegexpTokenizer
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.tree import Tree
from nltk.chunk.regexp import RegexpParser
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.wsd import lesk



_tokenizer = RegexpTokenizer(r'\w+')
_lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))
_hyper = lambda sense: sense.hypernyms()
_hypo = lambda sense: sense.hyponyms()
_parser = RegexpParser(""" NP: {<DT>?<JJ>*<NN>}
                  {<NNP>+}
                  {<NN><NN>}
                  {<NNS><VBP>}
                  {<V.*> <TO> <V.*>}
                  {<N.*>(4,)} """)


def shallowParse(word_tags):
    words = set()
    parse_tree = _parser.parse(word_tags)
    for sub_tree in parse_tree:
        if type(sub_tree) is Tree and sub_tree.label() == 'NP':
            words |= {word for word, tag in sub_tree.leaves() if 'NN' in tag or 'VB' in tag or 'JJ' in tag}
    return words


def getBestSenses(review, words):
    senses = []
    for word in words:
        sense = lesk(review, word)
        if sense is not None:
            senses += [sense]
    return senses


def getLemmaNames(senses):
    words = set()
    for sense in senses:
        words |= set(sense.lemma_names())
    return words


def getHypernyms(senses):
    hypers = set()
    for sense in senses:
        hypers |= set(list(sense.closure(_hyper))[:2])
    return getLemmaNames(hypers)


def getHyponyms(senses):
    hypos = set()
    for sense in senses:
        hypos |= set(list(sense.closure(_hypo))[:2])
    return getLemmaNames(hypos)


def addFeatures(featureSet, features):
    for feature in features:
        if feature not in featureSet:
            featureSet[feature] = 1
#        featureSet[feature] += 1


def extractFeatures(data_file, flag=False):
    featureSets = []
    prodLabels = []
    sentiLabels = []

    with open(data_file, 'r') as reviews:
        for review in reviews:
            featureSet = {}
            prodLabel = ''
            sentiLabel = ''
            reviewTag = review.split('__')

            if (len(reviewTag) > 1):
                reviewSplit = reviewTag[0].lower().split('_')
                prodLabel = reviewSplit[0]
                sentiLabel = reviewSplit[1]
                review = reviewTag[1]
            if flag:
                print review
            review = review.lower()

            # Lexical feature 1 : Tokenize
            words = _tokenizer.tokenize(review)
            if flag:
                print words

            # Lexical feature 2 : Remove Stopwords
            words = [word for word in words if word not in STOPWORDS]
            if flag:
                print words

            # Syntactic feature 1 : POS Tags
            word_tags = pos_tag(words)
            if flag:
                print word_tags

            # Syntactic feature 2 : Shallow Parsing
            words = shallowParse(word_tags)
            if flag:
                print words

            # Lexical feature 3 : Lemmatize (noun singular & verb base form)
            words = [_lemmatizer.lemmatize(_lemmatizer.lemmatize(word), 'v') for word in words]
            addFeatures(featureSet, words)
            if flag:
                print featureSet

            # Semantic feature 1 : Word Sense Disambiguation
            senses = getBestSenses(review, words)
            words = getLemmaNames(senses)
            addFeatures(featureSet, words)
            if flag:
                print featureSet

            # Semantic feature 2
            addFeatures(featureSet, getHypernyms(senses))
            if flag:
                print featureSet

            # Semantic feature 3
            addFeatures(featureSet, getHyponyms(senses))
            if flag:
                print featureSet

            featureSets += [featureSet]
            prodLabels += [prodLabel]
            sentiLabels += [sentiLabel]

    return (featureSets, prodLabels, sentiLabels)
