# RMN_Omri

1. Run BookNLP or another NER (Name-Entity Recognition) tool.
2. Create a names file with the NER output, where each line is composed 
   of the different names of the same entity separated with 
   at least a space (can use a comma).

   For Example:


   Harry Potter    Potter    Mr Potter
   
   Ron Wiesley     Wiesly    Ron    
   

3. Update Definitions File with the different file paths and 
   the amount of entities needs to be analized (the tool will analize the 
   most <Definitions.num_of_entities> reffered entities in the book).
4. Run the run.sh script.



### Done automatically in spans_partition:

1. Change spans xlsx file to csv and gzip it. Then move it to the data dir in rmn repo with
   the name "relationships.csv.gz".
2. Take the "wmap_cmap_bmap.pkl" file from "RMN_Omri" dir to the data dir in rmn repo and change its name to "metadata.pkl".