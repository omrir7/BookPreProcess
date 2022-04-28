#!/usr/bin/env python3

#pre running tasks:

#1. the run script needs to be run after the BookNLP run and after the creation of the names part to a txt file
#2. after this the files pathes needs to be updated on the Definitions file.

# Python Scripts:
#1. removing stop words from the raw book .txt file.
python Remove_StopWords.py


#2. Parsing the names file
python Parsing_Names.py

#Partioning of the spans
python Spans_Partition.py

read