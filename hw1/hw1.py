import re
import sys
from nltk import sent_tokenize
import nltk

FILE_NAME = sys.argv[1]

def process_text():
    fp = open(FILE_NAME)
    content = fp.read()
    return content

def process_text_tokenize():
    fp = open(FILE_NAME)
    content = fp.read()
    content = tokenize(content)
    print content
    return content

def expand_contractions(s, contractions_re, contractions_dict):
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, s)

#This will tokenize words and remove leading and trailing punctuation into tokens
def tokenize(content):
    contractions = {"n't":" not", "'ll":" will", "'ve":" have", "'d":" would", "'re":" are", }
    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))
    content = re.sub(r"(I'm)", "I am", content)
    content = expand_contractions(content, contractions_re, contractions)
    tokens = re.findall(r"^[^\w\s]+|[A-Za-z'-]+|[^\w\s]", content)
    print tokens





def get_number_of_paragraphs(file_content):
    print "of paragraphs"
    split = file_content.split("\n\n")
    count = 0
    for paragraph in enumerate(split, 1):
        count += 1
    print count


def get_number_of_sentences(file_content):
    print "of sentences"
    num_sentences = len(re.findall(r'[?!.]+', file_content))
    print num_sentences


def get_number_of_words(file_content):
    print "of tokens"



def get_number_of_distinct_words():
    print "of types"


def get_word_frequency(word):
    print "Get word " + word + " frequency"


tokenized = process_text_tokenize()
non_tokenized = process_text()
#get_number_of_paragraphs(non_tokenized)
#get_number_of_sentences(non_tokenized)
get_number_of_words(tokenized)
get_number_of_distinct_words()
get_word_frequency("THIS")
