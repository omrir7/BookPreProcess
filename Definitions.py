
#book name
book_name = "PerfectPeace"

#book .txt file path - input to Remove_StopWrods
book_txt_path = "../BookNLP/A Perfect Peace/A Perfect Peace.txt"

#book .txt file without stop words
no_stop_words_path = '../BookNLP/A Perfect Peace/A Perfect Peace - NoStopWords.txt'

#raw names file - Input od Parsing_Names
raw_names_file_path = "../BookNLP/A Perfect Peace/outputdir/Names"

#names parsed path - output of Parsing_Names
parsed_names_path = '../BookNLP/A Perfect Peace/outputdir/Names_Parsed'

#how many characters will be evaluated (number of most referenced entities that will be evaluated)
num_of_entities = 3

#entities structure - 2d
entities_all = "entities.pkl"

#number of entities to comapre to
entities_to_cmp = 18

#excel output filw path - output of spans Partition
excel_path = 'spans_PerfectPeace.xlsx'

#Minimun amount of spans in dir to participate in the model training
min_spans = 7
#minimu, length of span
min_span_length = 5
#Metadata Path
Metadata_Path = "../rmn/data/metadata.pkl"

#csv path
csv_path = "../rmn/data/relationships.csv"


#NER TESTS
flair_ner_file = "../BookNLP/A Perfect Peace/outputdir/Names_flair.pkl"
spacy_ner_file = "../BookNLP/A Perfect Peace/outputdir/Names_spacy.pkl"