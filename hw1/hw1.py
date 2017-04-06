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
    return content

def expand_posessives(content):
    posessives = re.findall(r"([a-zA-Z'-]+\'s)", content)
    posessive_tokens = {}
    for posessive in posessives:
        posessive_tokens[posessive] = [posessive.split("'")[0], "'" + posessive.split("'")[1]]

    for key, value in posessive_tokens.iteritems():
        content = expand(key, str(value[0] + " " + value[1]), content)
    return content

def expand_other(content):
    other_contractions={"Here's": "Here is", "What's": "What is", "Who's": "Who is", "Let's": "Let us", "That's": " That is", "There's": "There is", "I'm": "I am", "He's": "He is", "She's": "She is", "It's": "It is"}
    for key, value in other_contractions.iteritems():
        content = expand(key, value, content)
        content = expand(key.lower(), value.lower(), content)
    return content

def expand(contraction, expanded, content):
    contraction_re = re.compile('(%s)' % contraction)
    return re.sub(contraction_re, expanded, content)

def expand_contractions(s):
    contractions = {"n't": " not", "'ll": " will", "'ve": " have", "'d": " would", "'re": " are", }
    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))
    def replace(match):
        return contractions[match.group(0)]
    return contractions_re.sub(replace, s)

#This will tokenize words and remove leading and trailing punctuation into tokens
def tokenize(content):
    content = expand_other(content)
    content = expand_contractions(content)
    content = expand_posessives(content)
    tokens = re.findall(r"^[^\w\s]+|[A-Za-z0-9'-]+|[^\w\s]", content)
    return tokens





def get_number_of_paragraphs(file_content):
    split = file_content.split("\n\n")
    count = 0
    for paragraph in enumerate(split, 1):
        count += 1
    return "#of paragraphs = " + str(count) + "\n"


def get_number_of_sentences(file_content):

    num_sentences = len(re.findall(r'[?!.]+', file_content))
    return "# of sentences = "  + str(num_sentences) + "\n"


def get_number_of_words(file_content):
    return "# of tokens = " + str(len(file_content)) + "\n"



def get_number_of_distinct_words(file_content):
    return "# of types = " + str(len(set(file_content))) + "\n"


def get_word_frequency(token_list, f):
    frequency_dict= {}
    freq_list = []
    token_list = sorted(token_list)
    for i in token_list:
        print(i, token_list.count(i))

    return freq_list



def parse_and_print():
    tokenized = process_text_tokenize()
    non_tokenized = process_text()
    f = open('output-' + FILE_NAME + '', 'w')
    f.write(get_number_of_paragraphs(non_tokenized))
    f.write(get_number_of_sentences(non_tokenized))
    f.write(get_number_of_words(tokenized))
    f.write(get_number_of_distinct_words(tokenized))
    f.write('=======================================================\n')
    get_word_frequency(tokenized, f)
    f.close()


parse_and_print()