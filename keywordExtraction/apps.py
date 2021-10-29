from django.apps import AppConfig

import yake
from rake_nltk import Rake

class KeywordextractionConfig(AppConfig):

	name = 'keywordExtraction'
	language = "en"
	max_ngram_size = 1
	deduplication_thresold = 0.9
	deduplication_algo = 'seqm'
	windowSize = 1
	numOfKeywords = 10
	custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)

	
	def yakeExtraction():
		name = 'keywordExtraction'
		language = "en"
		max_ngram_size = 1
		deduplication_thresold = 0.9
		deduplication_algo = 'seqm'
		windowSize = 1
		numOfKeywords = 10
		return yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)

	def rakeExtraction(text):
		r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
		custom_kw_extractor = r.extract_keywords_from_text(text)