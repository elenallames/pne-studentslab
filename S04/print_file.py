from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "sequences/RNU6_269P.fa"

# -- Open and read the file
file_contents = Path(FILENAME).read_text()

list_contents = file_contents.split("\n")
list_contents.pop(0) #remove header
# -- Print the contents on the console
print("".join(file_contents))

#Another option
index = file_contents.find("\n")
file_contents = (file_contents[index:]).replace("\n", "")
print(len(file_contents))
