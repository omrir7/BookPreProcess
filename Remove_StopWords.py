import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import words

# word_tokenize accepts
# a string as an input, not a file.
stop_words = set(stopwords.words('english'))
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace.txt", encoding="mbcs")

# Use this to read file content as a stream:
line = file1.read()
tokens = line.split()


for r in tokens:
    if not r in stop_words:
        appendFile = open('C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace - NoStopWords.txt', 'a', encoding="mbcs")
        appendFile.write(" " + r)
        appendFile.close(   )