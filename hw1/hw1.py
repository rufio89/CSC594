#RYAN KRIENITZ
import re
import sys
from collections import Counter
from nltk import sent_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')

INPUT_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME =  sys.argv[2]

def process_text():
    fp = open(INPUT_FILE_NAME)
    content = fp.read().decode('utf8')
    return content

def process_text_tokenize():
    fp = open(INPUT_FILE_NAME)
    content = fp.read().decode('utf8')
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
    acronyms = ["Dr.", "D.J.", "Mr."]
    count = 0
    for item in file_content:
        if not item.rsplit(None, 1)[-1] in acronyms:
            count +=1

    return "# of sentences = " + str(count) + "\n"



def get_number_of_words(file_content):
    return "# of tokens = " + str(len(file_content)) + "\n"



def get_number_of_distinct_words(file_content):
    return "# of types = " + str(len(set(file_content))) + "\n"


def get_word_frequency(token_list, f):
    freq_list = dict(Counter(token_list))
    sorted_tokens = sorted(freq_list.iteritems(), key=lambda kv: kv[1], reverse=True)
    for key, value in sorted_tokens:
        f.write(str(key) + " " +  str(value) + "\n")



def parse_and_print():
    tokenized = process_text_tokenize()
    non_tokenized = process_text()
    f = open(OUTPUT_FILE_NAME, 'w')
    f.write(get_number_of_paragraphs(non_tokenized))
    f.write(get_number_of_sentences(sent_tokenize(non_tokenized)))
    f.write(get_number_of_words(tokenized))
    f.write(get_number_of_distinct_words(tokenized))
    f.write('=======================================================\n')
    get_word_frequency(tokenized, f)
    f.close()


parse_and_print()