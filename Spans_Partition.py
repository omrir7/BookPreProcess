# inputs:
#  1. text file without stop words
#  2. names file
#  output:
#  spans excel

#This files gets a text file with no stop words and partioning this text to spans with maximum 200 tokens.
# a token beggins 100 tokens before a mention of a entity (or with a different entity) and ends 100 tokens
# after the reference or with another entity. A span will not include more than 2 entities.





############
#current issue is that I have entities before the first analized entyyty that are not suppose to be included
#


from collections import OrderedDict
import pandas as pd
import re
import pickle
import Definitions
import xlrd as xlrd
import csv
import gzip

import to_one_reference

class span:
    def __init__(self,text, first_entity_idx, last_span_end_idx, names, entities_all):
        self.characters = []
        self.tokens     = []
        self.length     = 0
        self.endIdx     = 0
        self.first_character_idx = first_entity_idx
        self.delete_span = 0
        l = len(text)
        if (first_entity_idx < l):
            first_entity_in_entities_array = index_2d(names, text[first_entity_idx])
            self.characters.append(text[first_entity_idx])
        # the first word of the next span is eather 100 words ago or the last span end if it is closer
        if (first_entity_idx - 100 < last_span_end_idx):
            cur_first_word_idx = last_span_end_idx
        else:
            cur_first_word_idx = first_entity_idx - 100
        self.tokens = []
        # left half of the span
        for i in range(cur_first_word_idx, first_entity_idx):  # new_omri
            if (index_2d(entities_all, text[i]) is False):
                self.tokens.append(text[i])
        # tokens=text[cur_first_word_idx:first_entity_idx] #old

        # right half of the span
        i = first_entity_idx
        if (i >= l):
            self.delete_span = 1
            return

        entity_appear = index_2d(names, text[i])
        # while i didnt get 100 tokens after the first entity, and i didnt see a DIFFERENT entity
        while i < first_entity_idx + 100 and (entity_appear is False or entity_appear == first_entity_in_entities_array):
            if (index_2d(entities_all, text[i]) is False):
                self.tokens.append(text[i])
            i += 1
            if (i >= l):
                #self.delete_span = 1
                break
            entity_appear = index_2d(entities_all, text[i])  # omri
        # if I didnt find another entity in the next 100 tookens after the first entity so this is not a good span
        if i >= first_entity_idx + 100:
            self.delete_span = 1
            return
        if (i >= l):
            self.delete_span = 1
            return
        if entity_appear >= Definitions.num_of_entities:
            self.delete_span = 1
            return
        # if i found the second entity which is not identical to the first one
        if entity_appear is not False:
            # while i didnt find the second entity or i found and entity identical to the first one
            while entity_appear is not False or (entity_appear is False and i < first_entity_idx + 100):
                if (entity_appear is not False) and (entity_appear >= Definitions.num_of_entities):
                    self.delete_span = 1
                    return
                if (entity_appear is not False and entity_appear != first_entity_in_entities_array):
                    self.characters.append(text[i])
                    second_entity_in_entities_array = entity_appear
                    if (index_2d(entities_all, text[i]) is False):
                        self.tokens.append(text[i])
                    i += 1
                    entity_appear = index_2d(names, text[i])
                    # keep going after the second entity until another name or 100 tokens after the first name
                    while i < first_entity_idx + 100 and (entity_appear is False or entity_appear == first_entity_in_entities_array or entity_appear == second_entity_in_entities_array):
                        i += 1
                        if (i <= len(text) - 50):
                            if (index_2d(entities_all, text[i]) is False):
                                self.tokens.append(text[i])
                            entity_appear = index_2d(entities_all, text[i + 1])  # omri
                            if (entity_appear >= Definitions.num_of_entities):
                                break
                    break
                i += 1
                entity_appear = index_2d(names, text[i])

            # omri - if the second entity is not one of the analized ones
            if ((any(self.characters[0] in sublist for sublist in entities_all)) and not (any(self.characters[0] in sublist for sublist in names))) or ((any(self.characters[1] in sublist for sublist in entities_all)) and not (any(self.characters[1] in sublist for sublist in names))):
                self.delete_span = 1
                return
            # end of omri

            # appending the characters in this span to the output file, and the length of thi span
            self.tokens.append(self.characters)
            self.length = i - cur_first_word_idx
            if self.delete_span ==0:
                self.endIdx = i

#this function is dedicated to find if a word is from the 2d names array,
# if so it returns the entity index, for example, if an entity is called Yonatan Lifshitz and another one is called Yolek,
# "Yonatan" and "Lifshitz" will return the same value, but "Lifshitz" and "Yolek" will return different int values.
# the word "Table" will return false, because it is not a name from the names 2d list.
def index_2d(names2d, appearance):
    #if (appearance=="yonatan"):
      #  print(1)
    for i, x in enumerate(names2d):
        if appearance in x:
            return i
    return False


def spans_to_excel(ordered_spans,excel_path,book):
    spans_for_excel = []
    words_counter = 0
    characters_counter = 0
    books_counter = 0
    cmap = dict()
    wmap = dict()
    bmap = dict()
    for relationship in ordered_spans:
        span_id=0
        for span in relationship[1::]:
            cur_span = []
            characters = relationship[0]
            cur_span.append(book)
            if(book not in bmap):
                bmap[book] = books_counter
                books_counter+=1
            cur_span.append(characters[0])
            cur_span.append(characters[1])
            if(characters[0] not in cmap):
                cmap[characters[0]] = characters_counter
                characters_counter+=1
            if(characters[1] not in cmap):
                cmap[characters[1]] = characters_counter
                characters_counter+=1
            cur_span.append(span_id)
            del span[-3:] #removing characters names and span length
            span_string = ' '.join(str(v) for v in span) #from list of words to string
            span_string = re.sub(r'[^\w\s]', '', span_string)
            span_list = list(str.split(span_string))
            for word in span_list:
                if word not in wmap:
                    wmap[word] = words_counter
                    words_counter+=1
            cur_span.append(span_string)
            spans_for_excel.append(cur_span)
            span_id+=1
    columns=['Book', 'Char1', 'Char2', 'Span ID','Words']
    df = pd.DataFrame(spans_for_excel,columns=columns)
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='PP_Spans', index=False)
    writer.save()
    return wmap, cmap, bmap


#this function gets a spans object which is not ordered by characters. and returns a spans object that is ordered:
#spans_ordered_list[0] is a list of all the spans related to the characters appears in its 1st element.
def arrange_spans(spans,names):
    spans_dict = OrderedDict()
    del spans[-1]
    for cur_span in spans:
        index_first = index_2d(names,cur_span[-2][0])
        index_second = index_2d(names,cur_span[-2][1])
        key1 = str(index_first) + " " + str(index_second)
        key2 = str(index_second) + " " + str(index_first)
        key1_list = key1.split()
        key1_list = [int(i) for i in key1_list]
        key2_list = key2.split()
        key2_list = [int(i) for i in key2_list]
        if key1 in spans_dict or key2 in spans_dict:
            spans_dict[key1].append(cur_span)
            spans_dict[key2].append(cur_span)
        else:
            spans_dict[key1] = []
            spans_dict[key2] = []
            #handle [Yoni,Hava] <-> [Hava,Yoni] identicality
            if (key1<key2):
                spans_dict[key1].append([names[int(key1_list[0])][0],names[int(key2_list[0])][0]])
                spans_dict[key2].append([names[int(key1_list[0])][0],names[int(key2_list[0])][0]])
            else:
                spans_dict[key1].append([names[int(key2_list[0])][0], names[int(key1_list[0])][0]])
                spans_dict[key2].append([names[int(key2_list[0])][0], names[int(key1_list[0])][0]])
            spans_dict[key1].append(cur_span)
            spans_dict[key2].append(cur_span)
    dict_keys = list(spans_dict.keys())
    del dict_keys[1::2]
    spans_ordered_list=[]
    for key in dict_keys:
        spans_ordered_list.append(spans_dict[key])
    #remove spans with less than 7 spans (noisy)
    spans_ordered_list = [item for item in spans_ordered_list if len(item) >= Definitions.min_spans]
    return spans_ordered_list







print("Generating Entities Structure...",end =" ")
file1 = open(Definitions.parsed_names_path, encoding="utf-8")
entities = []
for line in file1:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  entities.append(line_list)
file1.close()
print("Done!")


print("keep only N most appearances from names file...",end =" ")
entities_all = entities[0:(Definitions.entities_to_cmp-1)] #only not analized
entities = entities[0:Definitions.num_of_entities]


print("Spans Partitioning...",end =" ")
file1 = open(Definitions.no_stop_words_path, encoding="utf-8")
line = file1.read()  #characters
words = line.split() #words
print("Running to_one_reference Script...", end=" ")
words = to_one_reference.one_ref(words,entities_all)
i=0
spans=[]
spans_counter=0
last_span_end_idx = 0
last_not_include_entity = 0
while i<len(words):
    #omri
    #if (any(words[i] in sublist for sublist in entities_all) and not any(words[i] in sublist for sublist in entities)) :
    #    last_not_include_entity = i
    #end of omri
    entity_appear = index_2d(entities_all,words[i]) #omri

    while entity_appear is False:
        i+=1
        if(i>=len(words)):
            break
        entity_appear = index_2d(entities_all, words[i])
    if entity_appear>=Definitions.num_of_entities:
        last_not_include_entity=i+1
        i+=1
        continue
    first_character_idx = i
    if(last_span_end_idx<last_not_include_entity):
        last_span_end_idx=last_not_include_entity+1
    cur_span =span(words,i,last_span_end_idx,entities,entities_all)
    last_span_end_idx = cur_span.endIdx
    i+=1
    if cur_span.delete_span==0:
        spans.append(cur_span)
        i=cur_span.endIdx+1
    else:
        last_span_end_idx = cur_span.first_character_idx+100
        i=cur_span.first_character_idx+100


    #if end of the book, print to ouput file
    if i>=len(words):
        print("done")
        print("Writing To Excel file: "+str(Definitions.excel_path) +"....", end=" ")
        ordered_spans = arrange_spans(spans,entities)
        excel_path = Definitions.excel_path
        wmap, cmap, bmap = spans_to_excel(ordered_spans, excel_path,Definitions.book_name)
        with open(Definitions.Metadata_Path, "wb") as f:
            pickle.dump(wmap, f)
            pickle.dump(cmap, f)
            pickle.dump(bmap, f)
        print("done")
        break

#convert to csv and store in the rmn input dir
read_file = pd.read_excel(excel_path)
read_file.to_csv (Definitions.csv_path, index = None, header=True)

#gz the csv fiile
fp = open(Definitions.csv_path,"rb")
data = fp.read()
bindata = bytearray(data)
with gzip.open(Definitions.csv_path+".gz", "wb") as f:
    f.write(bindata)

