Natural Language Processing - Final Project

Review Classification & Sentiment Analysis
___________________________________________

Programming Language: Python 2.7
Third Party Tool: NLTK Stopwords and wordnet

Contents
--------
* Labels.py - module to contain various classification labels
* SimpleFeatureExtractor.py - basic feature extractor for Naive Bayes with no
							  NLP techniques
* AdvancedFeatureExtractor.py - improved feature extractor using NLP
* Main.py - driver module to run the project, uses Naive Bayes to train and
			test the data
* traindata.txt - tagged reviews for training
* testdata.txt - tagged reviews for testing

Command
-------
python main.py f p [tr] [te]

f 	: which feature extractor to use
	0 - Simple feature extractor
	1 - Advanced feature extractor
p 	: level of logging in the console
	0 - print only accuracy, precision & recall
	1 - print also the feature vectors at every step of the processing
tr  file path to training data. This is optional parameter. If it is not provided,
	application will look for trainingdata.txt in application folder.
te  file path to testing data. This is optional parameter. If it is not provided,
	application will look for testingdata.txt in application folder.