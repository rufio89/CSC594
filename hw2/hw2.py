from nltk.tokenize import sent_tokenize, word_tokenize
import sys
import collections
from nltk.tokenize import RegexpTokenizer

INPUT_FILE_NAME_TRAIN = sys.argv[1]
INPUT_FILE_NAME_TEST = sys.argv[1]


def process_text():
    fp = open(INPUT_FILE_NAME_TRAIN)
    content = fp.read()
    return content

def get_sentences():
    sentences = sent_tokenize(process_text())
    return sentences


def add_tokens(sentences):
    new_sentences = ""
    for s in sentences:
        new_sentences += "<s>" + s + "</s>"
    return new_sentences




def replace_token_symbols(words):
    word_total = len(words)
    index = 0
    while index < word_total:
        period_index = 0;
        first = words[int(index)]
        second = words[int(index) + 1]
        third = words[int(index) + 2]
        new_token = ""
        if first == "<" and second == "s" and third == ">":
            new_token = ''.join(words[int(index):int(index)+3])
            words[int(index)] = new_token
            words.remove(second)
            words.remove(third)
            word_total = word_total - 2
        if first == "<" and second == "/s" and third == ">":
            period = words[int(index)-1][len(words[int(index)-1])-1]
            words[int(index) - 1]  =  words[int(index) - 1][0:len(words[int(index)-1])-1]

            new_token = ''.join(words[int(index):int(index) + 3])
            words[int(index)] = period
            words[int(index)+1] = new_token
            words.remove(third)
            word_total = word_total - 2
        index = index + 1
    return words

def get_unique(words):
    new_list = []
    for token in words:
        if token not in new_list:
            new_list.append(token)

    return new_list


def get_unigram_set(words):
    word_count_dict = {}
    new_list = []

    for token in words:
        if token not in new_list:
            new_list.append(token)
            word_count_dict[token] = 1
        else:
            word_count_dict[token] = word_count_dict[token] + 1
    del word_count_dict["<s>"]
    return word_count_dict

def get_unigram_count(unigram_dict):
    n_val = 0
    for key, val in unigram_dict.iteritems():
        n_val+= val;

    return n_val

def get_unigram_probabilties(unique_words, unigram_dict, n):
    new_tokens = unique_words
    unigram_probability_dict = {}
    i=0
    new_tokens.remove("<s>")
    for index, value in enumerate(new_tokens):
       unigram_probability_dict[value] = unigram_dict[value] / n

    print unigram_probability_dict

#SENTENCES
sentences = get_sentences()
num_sentences = len(sentences)
#TOKENIZED LIST
words = word_tokenize(add_tokens(sentences))
#CREATES ACTUAL TOKEN SYMBOLS BECAUSE THEY GET SPLIT
#THIS IS GOOD LIST OF TOKENS TO LOOP THROUGH
words = replace_token_symbols(words)

#GETS THE UNIQUE SET
unique_words = get_unique(words)
#UNIGRAM VARS
unigram_dict = get_unigram_set(words)
unigram_n_count = get_unigram_count(unigram_dict)
unigram_v_count = len(unigram_dict)



# print num_sentences
# print unigram_dict
# print unigram_n_count
# print unigram_v_count
get_unigram_probabilties(unique_words, unigram_dict, unigram_n_count)


















