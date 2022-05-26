
from nltk.corpus import stopwords
import Definitions
import string
from gensim.parsing.preprocessing import remove_stopwords
from nltk.corpus import stopwords


print("Removing Stop Words From the raw .txt file" , end="\n")
# word_tokenize accepts
# a string as an input, not a file.
stop_words = set(stopwords.words('english'))
file1 = open(Definitions.book_txt_path, encoding="utf-8")

for word in stop_words:
    word = word.replace('\"', '')
    word = word.replace('“', '')
    word = word.replace('”', '')
    word = word.replace("’", '')
    word = word.replace('\'', '')

# Use this to read file content as a stream:
line = file1.read()
tokens = line.split()
tokens = [i.lower() for i in tokens]
words=[]
for r in tokens:
    r =  r.translate(str.maketrans('', '', string.punctuation))
    r = r.replace('\"', '')
    r = r.replace('“', '')
    r = r.replace('”', '')
    r = r.replace("’", '')
    r = r.replace('\'', '')
    if not r in stop_words:
        words.append(r)

textfile = open(Definitions.no_stop_words_path, "w", encoding="utf-8")
for element in words:
    textfile.write(element + " ")
textfile.close()


#appendFile = open(Definitions.no_stop_words_path, 'a', encoding="mbcs")
#appendFile.write(" " + r)
#appendFile.close(   )
print("Done")
