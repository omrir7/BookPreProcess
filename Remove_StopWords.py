
from nltk.corpus import stopwords
import Definitions



print("Removing Stop Words From the raw .txt file" , end=" ")
# word_tokenize accepts
# a string as an input, not a file.
stop_words = set(stopwords.words('english'))
file1 = open(Definitions.book_txt_path, encoding="mbcs")

# Use this to read file content as a stream:
line = file1.read()
tokens = line.split()

for r in tokens:
    if not r in stop_words:
        appendFile = open(Definitions.no_stop_words_path, 'a', encoding="mbcs")
        appendFile.write(" " + r)
        appendFile.close(   )
print("Done")
