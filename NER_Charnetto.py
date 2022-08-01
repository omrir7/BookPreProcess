import Definitions
import flair
import spacy
from flair.models import SequenceTagger
import pickle



import charnetto

# Use this to read file content as a stream:
with open(Definitions.book_txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in lines:
    if len(i)<4:
        del lines[lines.index(i)]

flair_df = charnetto.extract_flair_df(lines,SequenceTagger.load('ner'))
file_flair = open(Definitions.flair_ner_file, 'w')
pickle.dump(flair_df, file_flair)

#spacy_df = charnetto.extract_spacy_df(lines, spacy.load("en_core_web_lg"))
#file_spacy = open(Definitions.spacy_ner_file, 'w')
#pickle.dump(spacy_df, file_spacy)

print("done")
