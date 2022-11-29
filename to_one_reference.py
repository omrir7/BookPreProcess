

'''
Input:
1. txt file splited to tokens.
2. Entities list with the following structure:
      Entity1(name1)   Entity1(name2)   Entity1(name3)
      Entity2(name1)
      Entity3(name1)   Entity3(name2)

'''


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


example_tokens = "omri and aaaa aaa vvv rafaeli asdasd yaara asdokosa yaara omri romano yaara rafaeli sfoicf rafa kdsmckmcs rom akdkamck "
tokens = example_tokens.split()
example_entities = [["omri", "rafaeli","rafa"],["yaara","romano"]]

print(one_ref(tokens,example_entities))