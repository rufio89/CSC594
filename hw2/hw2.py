from nltk.tokenize import sent_tokenize, word_tokenize, TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk import bigrams, FreqDist, ngrams
from collections import Counter
from math import log, e, exp
import re
import sys
import collections
from nltk.tokenize import RegexpTokenizer
tokenizer = TreebankWordTokenizer()
tokenizer.PARENS_BRACKETS = [
    (re.compile(r'[\]\[\(\)\{\}]'), r' \g<0> '),
    (re.compile(r'--'), r' -- '),
    (re.compile(r'(<s>)([^\d])'), r' \1 \2'),
    (re.compile(r'(<s>)([^</s>])'), r' \1 \2'),
    (re.compile(r'(</s>)'), r' \1'),
]

tokenizer.PUNCTUATION = [
        (re.compile(r'([:,])([^\d])'), r' \1 \2'),
        (re.compile(r'([:,])$'), r' \1 '),
        (re.compile(r'\.\.\.'), r' ... '),
        (re.compile(r'[;@#$%&]'), r' \g<0> '),
        (re.compile(r'([^\.])(\.)([\]\)}>"\']*)\s*$'), r'\1 \2\3 '),
        (re.compile(r'[?!.]'), r' \g<0> '),

        (re.compile(r"([^'])' "), r"\1 ' "),
    ]

reload(sys)
sys.setdefaultencoding('utf-8')

INPUT_FILE_NAME_TEST = sys.argv[2]
INPUT_FILE_NAME_TRAIN = sys.argv[1]


def expand_contractions(s):
    contractions = {"n't": " not", "'ll": " will", "'ve": " have", "'d": " would", "'re": " are", }
    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))
    def replace(match):
        return contractions[match.group(0)]
    return contractions_re.sub(replace, s)

def process_text(text):
    fp = open(text)
    content = fp.read().decode('windows-1252')
    content = expand_contractions(content)
    return content



def get_sentences(text):
    sentences = sent_tokenize(process_text(text))
    return sentences


def add_tokens(sentences):
    new_sentences = ""
    for s in sentences:
        new_sentences += "<s>" + s + "</s>"
    return new_sentences




# def replace_token_symbols(words):
#     word_total = len(words)
#     index = 0
#     while index < word_total:
#         period_index = 0;
#         first = words[int(index)]
#         second = words[int(index) + 1]
#         third = words[int(index) + 2]
#         new_token = ""
#         if first == "<" and second == "s" and third == ">":
#             new_token = ''.join(words[int(index):int(index)+3])
#             words[int(index)] = new_token
#             words.remove(second)
#             words.remove(third)
#             word_total = word_total - 2
#         if first == "<" and second == "/s" and third == ">":
#             period = words[int(index)-1][len(words[int(index)-1])-1]
#             words[int(index) - 1]  =  words[int(index) - 1][0:len(words[int(index)-1])-1]
#
#             new_token = ''.join(words[int(index):int(index) + 3])
#             words[int(index)] = period
#             words[int(index)+1] = new_token
#             words.remove(third)
#             word_total = word_total - 2
#         index = index + 1
#     return words

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
        unigram_probability_dict[value] = log(unigram_dict[value],e) - log(n, e)
    return unigram_probability_dict


def get_bigram_count(bigrams):
    bigram_freq_dist = FreqDist(bigrams)
    bigram_count_dict = {}
    for k, v in bigram_freq_dist.items():
        bigram_count_dict[k] =  v
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
        bigram_probability = log(bigram_count,e) - log(unigram_count, e)
        bigram_probability_dict[phrase] = bigram_probability
    return bigram_probability_dict


def get_sentence_unigram_probabilities(tokens, unigram_probabilities):
    total_probability = 0.0
    probabilty_dict = {}
    for index, token in enumerate(tokens):
        if token not in unigram_probabilities:
            probability = 0.0
            total_probability += probability
            probabilty_dict[token] = exp(probability)
        elif index == 0 and token == "<s>":
            new_token = "</s>"
            probability = unigram_probabilities[new_token]
            total_probability = probability
            probabilty_dict[token] = exp(probability)
        elif token =="<s>":
            new_token = "</s>"
            probability = unigram_probabilities[new_token]
            total_probability += probability
            probabilty_dict[token] = exp(probability)
        else:
            probability = unigram_probabilities[token]
            total_probability += probability
            probabilty_dict[token] = exp(probability)
    total_probability = exp(total_probability)
    return total_probability

def get_sentence_bigram_probabilties(tokens, bigram_probabilties):
    total_probability = 0.0
    probabilty_dict = {}
    first = ""
    second = ""
    index = 0
    while index < len(tokens)-1:
        token = tokens[index]
        second = tokens[index + 1]
        bigram = (token, second)
        if bigram in bigram_probabilties:
            probability = bigram_probabilties[bigram]
            total_probability += probability
            probabilty_dict[bigram] = probability
        else:
            probability = 0.0
            total_probability += probability
            probabilty_dict[bigram] = probability
        index = index + 1

    total_probability = exp(total_probability)
    return total_probability


#SENTENCES
training_sentences = get_sentences(INPUT_FILE_NAME_TRAIN)
test_sentences = get_sentences(INPUT_FILE_NAME_TEST)
num_sentences = len(training_sentences)
#TOKENIZED LIST
tokens = tokenizer.tokenize(add_tokens(training_sentences))
#CREATES ACTUAL TOKEN SYMBOLS BECAUSE THEY GET SPLIT
#THIS IS GOOD LIST OF TOKENS TO LOOP THROUGH



#GETS THE UNIQUE SET
unique_words = get_unique(tokens)
# # #UNIGRAM VARS
unigrams = ngrams(tokens,1)
unigram_counts = get_unigram_count(tokens)
unigram_n_count = get_unigram_n(unigram_counts)
unigram_v_count = len(unigram_counts)
bigrams = bigrams(tokens)


unigram_probabilities = get_unigram_probabilties(unique_words, unigram_counts, unigram_n_count)
bigram_counts = get_bigram_count(bigrams)
bigram_probabilties = get_bigram_probabilties(unique_words, bigram_counts, unigram_counts)





def print_results():
    for index, sentence in enumerate(test_sentences):
        new_sentence = "<s>" + sentence + "</s>"
        test_tokens = tokenizer.tokenize(new_sentence)
        unigram_sentence_probability = get_sentence_unigram_probabilities(test_tokens, unigram_probabilities)
        bigram_sentence_probability = get_sentence_bigram_probabilties(test_tokens, bigram_probabilties)
        print "Sentence " + str(index) + ": " + sentence + "\n"
        print "unigram [Prob]" + str(unigram_sentence_probability)
        print "bigram [Prob]" + str(bigram_sentence_probability)
        print ""

print_results()












