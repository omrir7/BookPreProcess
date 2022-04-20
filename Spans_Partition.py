#This files gets a text file with no stop words and partioning this text to spans with maximum 200 tokens.
# a token beggins 100 tokens before a mention of a entity (or with a different entity) and ends 100 tokens
# after the reference or with another entity. A span will not include more than 2 entities.

#this function is dedicated to find if a word is from the 2d names array,
# if so it returns the entity index, for example, if an entity is called Yonatan Lifshitz and another one is called Yolek,
# "Yonatan" and "Lifshitz" will return the same value, but "Lifshitz" and "Yolek" will return different int values.
# the word "Table" will return false, because it is not a name from the names 2d list.
def index_2d(names2d, appearance):
    for i, x in enumerate(names2d):
        if appearance in x:
            return i
    return False

def generate_span(text,first_entity_idx,last_span_end_idx,names):
    l=len(text)
    if(first_entity_idx<l):
        first_entity_in_entities_array = index_2d(names,text[first_entity_idx])
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
    # if i found the second entity which is not identical to the first one
    if entity_appear is not False:
        # while i didnt find the second entity or i found and entity identical to the first one
        while entity_appear is not False or (entity_appear is False and i<first_entity_idx+100):
            if(entity_appear is not False and entity_appear!=first_entity_in_entities_array):
                characters.append("2 " +text[i])
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
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed", encoding="mbcs")
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
file1 = open("C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace - NoStopWords.txt", encoding="mbcs")
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
        with open('PerfectPeace_Spans/spans_PerfectPeace.txt', 'w',encoding="mbcs") as f:
            for item in spans:
                for word in item:
                    f.write("%s " % word)
                f.write("\n")
            f.write(str(len(spans)) + " Spans")
        f.close()
        break


