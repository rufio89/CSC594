import re
import sys
import os
from nltk import bigrams, FreqDist, ngrams
from nltk.corpus import conll2000
from nltk.chunk import conllstr2tree
from BigramChunker import BigramChunker
from UnigramChunker import UnigramChunker
from math import log, e, exp
from pprint import pprint

INPUT_FILE_NAME_TRAIN = sys.argv[1]
INPUT_FILE_NAME_TEST = sys.argv[2]
INPUT_FILE_NAME_TAGS = sys.argv[3]
POS_TAGS = []

def process_tags():
    fp = open(INPUT_FILE_NAME_TAGS)
    content = fp.read()
    tags = []
    for u in content.split():
        tags.append(u)
    return tags

def process_training_text(file_name):
    train_sents = conll2000.chunked_sents(os.getcwd() + "/" + file_name)
    return train_sents

def add_tags(list):
    start = ("<s>", "<START>")
    stop = ("</s>", "<STOP>")
    end = (u'.', u'.')
    list_len = len(list)
    for index, item in enumerate(list):
        if(index==0):
            list.insert(index, start)
        if(item==end):
            if(index < list_len):
                list.insert(index+1, stop)
                list.insert(index + 2, start)
            else:
                list.insert(index+1, stop)



def get_word_pos(train_sents):
    list = []
    list.extend((word, pos) for sent in train_sents for(word, pos) in sent.leaves())
    add_tags(list)
    return list

def get_pos(train_sents):
    list = []
    list.extend((pos) for (word, pos) in train_sents)
    return list

def get_words(train_sents):
    list = []
    list.extend((word) for (word, pos) in train_sents)
    return list

def get_num_tags(pos):
    new_pos = [x for x in pos if x != "<START>"]
    return new_pos

def get_number_of_sentences(pos_unique):
    matches = filter(lambda obj: obj == "<STOP>", pos_unique)
    return len(matches)

def get_number_of_words(words):
    new_words = [x for x in words if x != "<s>" and x != "</s>"]
    return new_words

def get_bigram_dict(bigrams):
    bigram_dict = {}
    for b in bigrams.items():
        if(b[0] != ('</s>', '<s>')):
            bigram_dict[b[0]] = b[1]
    return bigram_dict



POS_TAGS = process_tags()
#TRAIN VARS
train_sents = process_training_text(INPUT_FILE_NAME_TRAIN)
train_word_pos = get_word_pos(train_sents)
train_words = get_words(train_word_pos)
train_pos = get_pos(train_word_pos)

train_pos_unique = get_num_tags(train_pos)
#NUMBER OF POS TAGS
train_num_pos_tags = len(train_pos_unique)

#NUMBER OF TRAINING SENTENCES
num_train_sent = get_number_of_sentences(train_pos_unique)

train_num_of_words = get_number_of_words(train_words)

train_unigrams = ngrams(train_pos, 1)
train_unigram_freq_dist = FreqDist(train_unigrams)
train_unigram_dict = {k[0]:v for k,v in train_unigram_freq_dist.iteritems()}
#print unigram_dict

train_trans_bigrams = ngrams(train_pos,2)
train_trans_bigram_freq_dist = FreqDist(train_trans_bigrams)
train_trans_bigram_dict = {k[0]+"|" + k[1]:v for k,v in train_trans_bigram_freq_dist.iteritems()}

train_word_pos_bigrams = ngrams(train_word_pos,2)
train_word_pos_bigram_freq_dist = FreqDist(train_word_pos_bigrams)
train_word_pos_bigram_dict = {k[0][0] + "|" + k[0][1]:v for k,v in train_word_pos_bigram_freq_dist.iteritems()}




#TEST VARS
test_sents = process_training_text(INPUT_FILE_NAME_TEST)
test_word_pos = get_word_pos(test_sents)
test_words = get_words(test_word_pos)
test_pos = get_pos(test_word_pos)

test_pos_unique = get_num_tags(test_pos)
#NUMBER OF POS TAGS
test_num_pos_tags = len(test_pos_unique)

#NUMBER OF TRAINING SENTENCES
num_test_sent = get_number_of_sentences(test_pos_unique)

num_of_words = get_number_of_words(test_words)

test_unigrams = ngrams(test_pos, 1)
test_unigram_freq_dist = FreqDist(test_unigrams)
test_unigram_dict = {k[0]:v for k,v in test_unigram_freq_dist.iteritems()}
#print unigram_dict

test_trans_bigrams = ngrams(test_pos,2)
test_trans_bigram_freq_dist = FreqDist(test_trans_bigrams)
test_trans_bigram_dict = {k[0]+"|" + k[1]:v for k,v in test_trans_bigram_freq_dist.iteritems()}

test_word_pos_bigrams = ngrams(test_word_pos,2)
test_word_pos_bigram_freq_dist = FreqDist(test_word_pos_bigrams)
test_word_pos_bigram_dict = {k[0][0] + "|" + k[0][1]:v for k,v in test_word_pos_bigram_freq_dist.iteritems()}


#print bigram_dict

print num_train_sent
print train_num_pos_tags
print len(train_trans_bigram_freq_dist)
print len(train_num_of_words)
print len(set(train_num_of_words))




def parse_unkowns(train, train_pos, train_unigram_dict):
    new_train = train
    new_unigram = train_unigram_dict
    for item in POS_TAGS:
        if item not in train_pos:
            new_train["<UNK>|" + str(item)] = 1
            new_unigram[str(item)] = 1
    return new_train, new_unigram


def transition_prob(bigram_freq_dist, unigram_dict):
    trans_probability_dict = {}
    for key, value in bigram_freq_dist.items():
        first_token = key[0:key.index('|')]
        second_token = key[key.index('|')+1:len(key)]
        bigram_count = value
        phrase = (second_token, first_token)
        if phrase != ('<START>', '<STOP>'):
            unigram_count = unigram_dict[first_token]
            probability = log(bigram_count,e) - log(unigram_count, e)
            trans_probability_dict[phrase] = probability
    return trans_probability_dict

#pprint(transition_prob(train_trans_bigram_dict, train_unigram_dict))

def emission_prob(test_word_bigram_freq_dist, unigram_dict):
    emission_probability_dict = {}
    for key, value in test_word_bigram_freq_dist.items():
        first_token = key[0:key.index('|')]
        second_token = key[key.index('|')+1:len(key)]
        bigram_count = value
        phrase = (first_token, second_token)
        if phrase != ('<START>', '<STOP>'):
            if second_token not in unigram_dict:
                unigram_count=1
            else:
                unigram_count = unigram_dict[second_token]
            probability = log(bigram_count,e) - log(unigram_count, e)
            emission_probability_dict[phrase] = probability
    return emission_probability_dict

emission_train, emission_unigram = parse_unkowns(train_word_pos_bigram_dict, train_pos, train_unigram_dict)
pprint(emission_prob(emission_train, emission_unigram))
