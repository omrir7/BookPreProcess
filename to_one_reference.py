

'''
Input:
1. txt file splited to tokens.
2. Entities list with the following structure:
      Entity1(name1)   Entity1(name2)   Entity1(name3)
      Entity2(name1)
      Entity3(name1)   Entity3(name2)

'''

import Definitions
def index_2d(names2d, appearance):
    #if (appearance=="yonatan"):
      #  print(1)
    for i, x in enumerate(names2d):
        if appearance in x:
            return i
    return False


def one_ref(txt, entities):
    for i in range(0,len(txt)):
        entity_apear = index_2d(entities,txt[i])
        if entity_apear is not False:
            txt[i] = entities[entity_apear][0]
    return txt



print("Running to_one_reference Script...", end=" ")
file1 = open(Definitions.parsed_names_path, encoding="utf-8")
entities = []
for line in file1:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  entities.append(line_list)
file1.close()
print("Done!")

file1 = open(Definitions.no_stop_words_path, encoding="utf-8")
line = file1.read()  #characters
words = line.split() #words
file1.close()

entities_all = entities[0:(Definitions.entities_to_cmp-1)]
words = one_ref(words,entities_all)

i=0
textfile = open(Definitions.no_stop_words_path, "w", encoding="utf-8")
for element in words:
    textfile.write(element + " ")
    i+=1
    if(i%30 ==0):
        textfile.write('\n')
textfile.close()
