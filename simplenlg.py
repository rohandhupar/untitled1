from nltk.tokenize import  sent_tokenize,word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import language_check
import codecs
with codecs.open("adzis.txt",'r',encoding='latin-1') as f:
    text = f.read()
def input_file_lines(input_text, tokens):
    tokens = input_text.splitlines()
    return tokens
data=input_file_lines(text,[])

# Method to check a given sentence for given rules
def checkSentence(string):
    # Calculate the length of the string.
    length = len(string)

    # Check that the first character lies in [A-Z].
    # Otherwise return false.
    if string[0] < 'A' or string[0] > 'Z':
        return False

    # If the last character is not a full stop(.) no
    # need to check further.
    if string[length - 1] != '.':
        return False

    # Maintain 2 states. Previous and current state based
    # on which vertex state you are. Initialise both with
    # 0 = start state.
    prev_state = 0
    curr_state = 0

    # Keep the index to the next character in the string.
    index = 1

    # Loop to go over the string.
    while (string[index]):
        # Set states according to the input characters in the
        # string and the rule defined in the description.
        # If current character is [A-Z]. Set current state as 0.
        if string[index] >= 'A' and string[index] <= 'Z':
            curr_state = 0

        # If current character is a space. Set current state as 1.
        elif string[index] == ' ':
            curr_state = 1

        # If current character is a space. Set current state as 2.
        elif string[index] >= 'a' and string[index] <= 'z':
            curr_state = 2

        # If current character is a space. Set current state as 3.
        elif string[index] == '.':
            curr_state = 3

        # Validates all current state with previous state for the
        # rules in the description of the problem.
        if prev_state == curr_state and curr_state != 2:
            return False

        # If we have reached last state and previous state is not 1,
        # then check next character. If next character is '\0', then
        # return true, else false
        if prev_state == 2 and curr_state == 0:
            return False

        # Set previous state as current state before going over
        # to the next character.
        if curr_state == 3 and prev_state != 1:
            return True

        index += 1

        prev_state = curr_state

    return False
# first passing data in to sentence_tokenizer then we will pass it to grammar checker to see the validity
sent=sent_tokenize(text)
string_size = len(sent)
print(string_size)
count_good=0
count_bad=0
valid_sent=[]
for i in xrange(string_size):
    if checkSentence(sent[i]):
        valid_sent.append(sent[i])
        count_good+=1
    else:
        count_bad+=1
import re
# preprocessing done
def preprocess(sentence):
    stopwords_en = set(stopwords.words('english'))

    sents_rm_stopwords = []
    for sent in sentence:
        sents_rm_stopwords.append(' '.join(w for w in word_tokenize(sent) if w.lower() not in stopwords_en))
    return sents_rm_stopwords
filter_w=preprocess(valid_sent)
print(filter_w)
from nltk.stem.porter import PorterStemmer
# stemming done
def stemming(stop_sent):
    porter = PorterStemmer()
    stemmed=[]
    for sent in stop_sent:
        stemmed.append(' '.join(porter.stem(w) for w in word_tokenize(sent)))
    return stemmed
# parsing done
final_join=stemming(filter_w)
print(final_join)
from pattern.en import parsetree
for sentence in (final_join):
    s = parsetree(sentence)
    for chunk_sent in s:
        for chunk in chunk_sent.chunks:
             for word in chunk.words:
                 print word,
             print

from pattern.search import search,match


matched=[]
templates = ['VB NP']
for sentence in (valid_sent):
    s = parsetree(sentence)
    for i in templates:
        if search(i,s):
           print search(i,s)
           matched.append(sentence)
import nltk
print(matched)
#qu_pre=['Why','Do you know why','What','How','When','Where']
cleanmatched=[]

from textclean.textclean import textclean
for i in matched:
    clean = textclean.clean(i)
    cleanmatched.append(clean)
mapping={}
output_str=""
output=[]
print(cleanmatched)
for i in cleanmatched:
    is_imperative=nltk.pos_tag(nltk.word_tokenize(i))
    for word , tag in is_imperative:
        if (tag=='VB' or tag=='NN'):
            output_str+=word + " "




    mapping[i]=output_str
    output_str = ""

df=pd.DataFrame(mapping.items(),columns=["sentence_input","sentence_ouput"])

df.to_csv("imperative_generate.csv")



