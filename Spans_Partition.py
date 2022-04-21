# inputs:
#  1. text file without stop words
#  2. names file
#  output:
#  spans excel

#This files gets a text file with no stop words and partioning this text to spans with maximum 200 tokens.
# a token beggins 100 tokens before a mention of a entity (or with a different entity) and ends 100 tokens
# after the reference or with another entity. A span will not include more than 2 entities.
from collections import OrderedDict
import pandas as pd
import string
import re



#this function is dedicated to find if a word is from the 2d names array,
# if so it returns the entity index, for example, if an entity is called Yonatan Lifshitz and another one is called Yolek,
# "Yonatan" and "Lifshitz" will return the same value, but "Lifshitz" and "Yolek" will return different int values.
# the word "Table" will return false, because it is not a name from the names 2d list.
def index_2d(names2d, appearance):
    for i, x in enumerate(names2d):
        if appearance in x:
            return i
    return False


def spans_to_excel(ordered_spans,excel_path,book):
    spans_for_excel = []
    for relationship in ordered_spans:
        span_id=0
        for span in relationship[1::]:
            cur_span = []
            characters = relationship[0]
            cur_span.append(book)
            cur_span.append(characters[0])
            cur_span.append(characters[1])
            cur_span.append(span_id)
            del span[-3:] #removing characters names and span length
            span_string = ' '.join(str(v) for v in span) #from list of words to string
            span_string = re.sub(r'[^\w\s]', '', span_string)
            cur_span.append(span_string)
            spans_for_excel.append(cur_span)
            span_id+=1
    columns=['Book', 'Char1', 'Char2', 'Span ID','Words']
    df = pd.DataFrame(spans_for_excel,columns=columns)
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='PP_Spans', index=False)
    writer.save()


#this function gets a spans object which is not ordered by characters. and returns a spans object that is ordered:
#spans_ordered_list[0] is a list of all the spans related to the characters appears in its 1st element.
def arrange_spans(spans,names):
    spans_dict = OrderedDict()
    for cur_span in spans:
        index_first = index_2d(names,cur_span[-2][0])
        index_second = index_2d(names,cur_span[-2][1])
        key1 = str(index_first) + " " + str(index_second)
        key2 = str(index_second) + " " + str(index_first)
        if key1 in spans_dict or key2 in spans_dict:
            spans_dict[key1].append(cur_span)
            spans_dict[key2].append(cur_span)
        else:
            spans_dict[key1] = []
            spans_dict[key2] = []
            if (key1<key2):
                spans_dict[key1].append([names[int(key1[0])][0],names[int(key2[0])][0]])
                spans_dict[key2].append([names[int(key1[0])][0],names[int(key2[0])][0]])
            else:
                spans_dict[key1].append([names[int(key2[0])][0], names[int(key1[0])][0]])
                spans_dict[key2].append([names[int(key2[0])][0], names[int(key1[0])][0]])
            spans_dict[key1].append(cur_span)
            spans_dict[key2].append(cur_span)
    dict_keys = list(spans_dict.keys())
    del dict_keys[1::2]
    spans_ordered_list=[]
    for key in dict_keys:
        spans_ordered_list.append(spans_dict[key])
    return spans_ordered_list
def generate_span(text,first_entity_idx,last_span_end_idx,names):
    l=len(text)
    if(first_entity_idx<l):
        first_entity_in_entities_array = index_2d(names,text[first_entity_idx])
        characters=[]
        characters.append(text[first_entity_idx])
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

    entity_appear = index_2d(names, text[i])
    #while i didnt get 100 tokens after the first entity, and i didnt see a DIFFERENT entity
    while i<first_entity_idx+100 and (entity_appear is False or entity_appear==first_entity_in_entities_array):
        cur_span.append(text[i])
        i+=1
        if(i>=l):
            break
        entity_appear = index_2d(names, text[i])
    #if I didnt find another entity in the next 100 tookens after the first entity so this is not a good span
    if i>=first_entity_idx+100:
        return False, False
    if (i >= l):
        return False, False
    # if i found the second entity which is not identical to the first one
    if entity_appear is not False:
        # while i didnt find the second entity or i found and entity identical to the first one
        while entity_appear is not False or (entity_appear is False and i<first_entity_idx+100):
            if(entity_appear is not False and entity_appear!=first_entity_in_entities_array):
                characters.append(text[i])
                cur_span.append(text[i])
                i+=1
                entity_appear = index_2d(names, text[i])
                #keep going after the second entity until another name or 100 tokens after the first name
                while(entity_appear is False and i<first_entity_idx+100):
                    i+=1
                    if(i<=75220):
                        entity_appear = index_2d(names, text[i])
                        cur_span.append(text[i])
                break
            cur_span.append(text[i])
            i+=1
            entity_appear = index_2d(names,text[i])

        # appending the characters in this span to the output file, and the length of thi span
        cur_span.append(characters)
        len_of_span = i-cur_first_word_idx
        cur_span.append(len_of_span)
        return cur_span,i





print("Generating Entities Structure...",end =" ")
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed", encoding="utf-8")
entities = []
for line in file1:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  entities.append(line_list)
file1.close()

flat_entities = [] #a flat list of all the entities
i=0
for sublist in entities:
    for item in sublist:
        flat_entities.append(item)
    i+=1
print("Done!")


print("keep only N most appearances from names file...",end =" ")
N=15
with open('C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed') as f1:
    lines = f1.readlines()
with open('C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed', 'w') as f2:
    f2.writelines(lines[0:N])
print("Done!")


print("Spans Partitioning...",end =" ")
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace - NoStopWords.txt", encoding="utf-8")
line = file1.read()  #characters
words = line.split() #words
i=0
spans=[]
spans_counter=0
last_span_end_idx = 0
while i<len(words):
    entity_appear = index_2d(entities,words[i])
    while entity_appear is False:
        i+=1
        if(i>=len(words)):
            break
        entity_appear = index_2d(entities, words[i])

    first_character_idx = i
    if(first_character_idx==75171):
        print(1)
    cur_span,i =generate_span(words,i,last_span_end_idx,entities)
    last_span_end_idx=i
    i+=1
    if cur_span is not False:
        spans.append(cur_span)
    else:
        last_span_end_idx = first_character_idx+100
        i=first_character_idx+100


    #if end of the book, print to ouput file
    if i>=len(words):
        ordered_spans = arrange_spans(spans,entities)
        excel_path = 'PerfectPeace_Spans/spans_PerfectPeace.xlsx'
        spans_to_excel(ordered_spans, excel_path,"PerfectPeace")



