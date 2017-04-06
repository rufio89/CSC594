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
    posessives = re.findall(r"(?=\S*['])([a-zA-Z'-]+)", content)
    posessive_tokens = {}
    for posessive in posessives:
        #posessive_tokens[posessive] = [posessive.split("'")[0], "'" + posessive.split("'")[1]]
        print posessive.split("'")

    for key, value in posessive_tokens.iteritems():
#       content = expand_other(key, str(value[0] + " " + value[1]), content)
        print key
        print value
    return content

def expand_personal_pronouns(content):
    other_contractions={"I'm": "I am", "He's": "He is", "She's": "She is", "It's": "It is"}
    for key, value in other_contractions.iteritems():
        content = expand_other(key, value, content)
        content = expand_other(key.lower(), value.lower(), content)
    return content

def expand_other(contraction, expanded, content):
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
    content = expand_personal_pronouns(content)
    content = expand_contractions(content)
    #content = expand_posessives(content)
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
    for word in token_list:
        frequency_dict[word] = token_list.count(word)
    sorted_frequency = sorted(frequency_dict.items(), key=lambda x: (-x[1], x[0]))
    for item in sorted_frequency:
        freq_list.append(str(item[0]) + " " + str(item[1]) + "\n")




def parse_and_print():
    tokenized = process_text_tokenize()
    non_tokenized = process_text()
    f = open('output-' + FILE_NAME + '', 'w')
    f.write(get_number_of_paragraphs(non_tokenized))
    f.write(get_number_of_sentences(non_tokenized))
    f.write(get_number_of_words(tokenized))
    f.write(get_number_of_distinct_words(tokenized))
    f.write('=======================================================\n')
    f.write(get_word_frequency(tokenized, f))
    f.close()


parse_and_print()