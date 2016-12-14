import sys
import SimpleFeatureExtractor
import AdvancedFeatureExtractor
from nltk.classify.util import accuracy
from nltk.classify import NaiveBayesClassifier
from collections import Counter
from Labels import PRODUCTS, SENTIMENTS
from tabulate import tabulate


def mapFeaturesToLabels(featureSets, labels):
    return [(featureSets[i], labels[i]) for i in xrange(len(featureSets))]


def getLabelIndices(labels, types):
    indices = {type:set() for type in types}
    for i in xrange(len(labels)):
        indices[labels[i]] |= {i}
    return indices


def trainAndTest(trFeatureSets, trLabels, teFeatureSets, teLabels, types, toPrint):
    classifier = NaiveBayesClassifier.train(mapFeaturesToLabels(trFeatureSets, trLabels))
    nuLabels = classifier.classify_many(teFeatureSets)
    if toPrint:
	    print 'Test labels:', teLabels
	    print 'New labels:', nuLabels
    print 'Accuracy: %.2f' % accuracy(classifier, mapFeaturesToLabels(teFeatureSets, teLabels))
    # classifier.show_most_informative_features()

    teIndices = getLabelIndices(teLabels, types)
    nuIndices = getLabelIndices(nuLabels, types)
    teCounts = Counter(teLabels)
    nuCounts = Counter(nuLabels)
    metrices = []
    for type in types:
        matches = len(teIndices[type] & nuIndices[type])
        precision = 1.0 * matches / nuCounts[type] if nuCounts[type] > 0 else '-'
        recall = 1.0 * matches / teCounts[type] if teCounts[type] > 0 else '-'
        metrices += [[type, precision, recall]]
    print tabulate(metrices, ['LABEL', 'PRECISION', 'RECALL'], tablefmt='fancy_grid', floatfmt='.2f')


if __name__ == '__main__':
	# select feature extractor
    featureExtractor = SimpleFeatureExtractor if sys.argv[1] == '0' else AdvancedFeatureExtractor

	# console print level   
    toPrint = False if sys.argv[2] == '0' else True

    # get the training data
    trainFile = 'traindata.txt' if len(sys.argv) < 4 else sys.argv[3]
    trFeatureSets, trProdLabels, trSentiLabels = featureExtractor.extractFeatures(trainFile)

    # get the testing data
    testFile = 'testdata.txt' if len(sys.argv) < 5 else sys.argv[4]
    teFeatureSets, teProdLabels, teSentiLabels = featureExtractor.extractFeatures(testFile, toPrint)

    # perform the naive based analysis
    print 'Product Classification'
    print '---------------------'
    trainAndTest(trFeatureSets, trProdLabels, teFeatureSets, teProdLabels, PRODUCTS, toPrint)
    print
    print 'Sentiment Analysis'
    print '------------------'
    trainAndTest(trFeatureSets, trSentiLabels, teFeatureSets, teSentiLabels, SENTIMENTS, toPrint)
