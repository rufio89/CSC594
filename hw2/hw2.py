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


def get_unigram_count(words):
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

def get_unigram_n(unigram_dict):
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
        unigram_probability_dict[value] = float(unigram_dict[value]) / float(n)
    return unigram_probability_dict


def get_bigram_count(words):
    new_list = []
    bigram_count_dict = {}
    first = ""
    second = ""
    phrase = ""
    index = 0
    while index < len(words)-1:
        first = words[index]
        second = words[index+1]
        phrase = (first, second)
        if phrase in new_list:
            bigram_count_dict[phrase] = bigram_count_dict[phrase] + 1
        else:
            bigram_count_dict[phrase] = 1
            new_list.append(phrase)
        index+=1
    del bigram_count_dict[("</s>", "<s>")]
    return bigram_count_dict


def get_bigram_probabilties(unique_words, bigram_counts, unigram_counts):
    new_bigram_counts = bigram_counts
    bigram_probability_dict = {}
    for key, value in bigram_counts.iteritems():
        first_token = key[0]
        second_token = key[1]
        bigram_count = value
        phrase = (first_token, second_token)
        # print "FIRST: " + str(first_token)
        # print "SECOND: " + str(second_token)
        # print "bigram_count: " + str(bigram_count)
        # print "PHRASE: " + str(phrase)
        if first_token == "<s>":
            first_token = "</s>"
        unigram_count = unigram_counts[first_token]
        bigram_probability = float(bigram_count) / float(unigram_count)
        bigram_probability_dict[phrase] = bigram_probability
    print bigram_probability_dict


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
unigram_counts = get_unigram_count(words)
unigram_n_count = get_unigram_n(unigram_counts)
unigram_v_count = len(unigram_counts)



# print num_sentences
# print unigram_counts
# print unigram_n_count
# print unigram_v_count
unigram_probabilities = get_unigram_probabilties(unique_words, unigram_counts, unigram_n_count)
bigram_counts = get_bigram_count(words)
get_bigram_probabilties(unique_words, bigram_counts, unigram_counts)
















