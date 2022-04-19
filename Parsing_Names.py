
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/PerfectPeace.book.html", encoding="mbcs")

# Use this to read file content as a stream:
line = file1.read()
words = line.split()

for r in line:
    appendFile = open('C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed', 'a',
                      encoding="mbcs")
    if not r in ["(" , ")" , "/", "1", "2", "3", "4", "5", "6" ,"7", "8","9" ,"0"]:
        appendFile.write(r)
    else:
        appendFile.write(" ")
    appendFile.close()

