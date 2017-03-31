import re
import sys
from nltk import sent_tokenize 
import nltk

FILE_NAME = sys.argv[1]

def process_text():
        print "Process Text"+ FILE_NAME
        fp = open(FILE_NAME)
        content = fp.read()
        FILE_CONTENT = sent_tokenize(content)
	return FILE_CONTENT

def get_number_of_paragraphs(file_content):
        print "Get Paragraphs"
	for word in file_content:
		print word


def get_number_of_sentences():
        print "Get number of sentences"


def get_number_of_words():
        print "get number of words"



def get_number_of_distinct_words():
        print "Get number of distinct words"


def get_word_frequency(word):
        print "Get word " + word + " frequency"



FILE_CONTENT = process_text()
get_number_of_paragraphs(FILE_CONTENT)
get_number_of_sentences()
get_number_of_words()
get_number_of_distinct_words()
get_word_frequency("THIS")
