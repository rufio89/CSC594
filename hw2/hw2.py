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

def add_tokens():
    sentences = sent_tokenize(process_text())
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



words = word_tokenize(add_tokens())
words = replace_token_symbols(words)
unique_words = get_unique(words)

print words
print unique_words










