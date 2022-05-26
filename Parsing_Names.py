import Definitions

print("Parsing Names File..." , end=" ")


#this file gets a file with the entities from the booknlp (first section of the .html file from the booknlp output dir)
file1 = open(Definitions.raw_names_file_path, encoding="mbcs")

# Use this to read file content as a stream:
line = file1.read()
words = line.split()

with open(Definitions.parsed_names_path, 'w',
                  encoding="mbcs") as f:
    for r in line:
        if not r in ["(" , ")" , "/",",", "1", "2", "3", "4", "5", "6" ,"7", "8","9" ,"0"]:
            f.write(r.lower())
        else:
            f.write(" ")
    f.close()

print("Done")

