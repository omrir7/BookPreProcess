#This files gets a text file with no stop words and partioning this text to spans with maximum 200 tokens.
# a token beggins 100 tokens before a mention of a entity (or with a different entity) and ends 100 tokens
# after the reference or with another entity. A span will not include more than 2 entities.
import pandas as pd
import pickle
import csv


def generate_span(text,first_entity_idx,last_span_end_idx,names):

    l=len(text)
    if(first_entity_idx<l):
        characters=[]
        characters.append("1 "+text[first_entity_idx])
    #the first word of the next span is eather 100 words ago or the last span end if it is closer
    if(first_entity_idx-100<last_span_end_idx):
        cur_first_word_idx=last_span_end_idx
    else:
        cur_first_word_idx=first_entity_idx-100
    #left half of the span
    cur_span=text[cur_first_word_idx:first_entity_idx]

    #right half of the span
    i=first_entity_idx
    if (i >= l):
        return [], i
    while i<first_entity_idx+100 and not (text[i] in names):
        cur_span.append(text[i])
        i+=1
        if(i>=l):
            break
    if not (text[i] in names):
        return False, False
    second_entity=0
    if (text[i] in names):
        second_entity=1
        while text[i] in names or ((not text[i] in names) and i<first_entity_idx+100):
            if(text[i] in names and second_entity==1):
                characters.append("2 " +text[i])
            else:
                second_entity=0
            cur_span.append(text[i])
            i+=1
        cur_span.append(characters)
        return cur_span,i





print("Generating Entities Structure...",end =" ")
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed", encoding="mbcs")
entities = []
for line in file1:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  entities.append(line_list)
file1.close()

flat_entities = [] #a flat list of all the entities
for sublist in entities:
    for item in sublist:
        flat_entities.append(item)
print("Done!")


print("keep only N most appearances from names file...",end =" ")
N=15
with open('C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed') as f1:
    lines = f1.readlines()
with open('C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed', 'w') as f2:
    f2.writelines(lines[0:N])
print("Done!")


print("Spans Partitioning...",end =" ")
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace - NoStopWords.txt", encoding="mbcs")
line = file1.read()  #characters
words = line.split() #words
i=0
spans=[]
spans_counter=0
last_span_end_idx = 0
while i<len(words):
    while not (words[i] in flat_entities):
        i+=1
        if(i>=len(words)):
            break
    cur_span,i =generate_span(words,i,last_span_end_idx,flat_entities)
    last_span_end_idx=i
    i+=1
    if cur_span!=False:
        spans.append(cur_span)
    if i>=len(words):
        with open('PerfectPeace_Spans/spans_PerfectPeace.txt', 'w',encoding="mbcs") as f:
            for item in spans:
                for word in item:
                    f.write("%s " % word)
                f.write("\n")
        f.close()
        break


