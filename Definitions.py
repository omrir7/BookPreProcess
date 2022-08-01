
#book name
book_name = "PerfectPeace"

#book .txt file path - input to Remove_StopWrods
book_txt_path = "C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace.txt"

#book .txt file without stop words
no_stop_words_path = 'C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/A Perfect Peace - NoStopWords.txt'

#raw names file - Input od Parsing_Names
raw_names_file_path = "C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names"

#names parsed path - output of Parsing_Names
parsed_names_path = 'C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_Parsed'
#how many characters will be evaluated (number of most referenced entities that will be evaluated)
num_of_entities = 4

#entities structure - 2d
entities_all = "PerfectPeace_Spans/entities.pkl"

#number of entities to comapre to
entities_to_cmp = 21

#excel output filw path - output of spans Partition
excel_path = 'PerfectPeace_Spans/spans_PerfectPeace.xlsx'

#Minimun amount of spans in dir to participate in the model training
min_spans = 7

#Metadata Path
Metadata_Path = "C:/Users/OmriRafaeli/PycharmProjects/NLP/rmn/data/metadata.pkl"

#csv path
csv_path = "C:/Users/OmriRafaeli/PycharmProjects/NLP/rmn/data/relationships.csv"

#NER TESTS
flair_ner_file = "C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_flair.pkl"
spacy_ner_file = "C:/Users/OmriRafaeli/PycharmProjects/NLP/BookNLP/A Perfect Peace/outputdir/Names_spacy.pkl"