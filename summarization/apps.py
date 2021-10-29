from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from django.apps import AppConfig

#from smmryapi import SmmryAPI

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

class SummarizationConfig(AppConfig):
    name = 'summarization'
    #SMMRY_API_KEY = '9E57E121E4'
    #smmry = SmmryAPI(SMMRY_API_KEY)
    LANGUAGE = "english"
    SENTENCES_COUNT = 10

    # url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    # parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    #text = "sample text"
    #parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    
    #stemmer = Stemmer(LANGUAGE)

    #summarizer = Summarizer(stemmer)
    #summarizer.stop_words = get_stop_words(LANGUAGE)

    def parser(text):
    	return PlaintextParser.from_string(text, Tokenizer("english"))


    def summarizer():
    	stemmer = Stemmer("english")
    	summarizer = Summarizer(stemmer)
    	summarizer.stop_words = get_stop_words("english")
    	return summarizer

    #for sentence in summarizer(parser.document, SENTENCES_COUNT):
    #    print(sentence)