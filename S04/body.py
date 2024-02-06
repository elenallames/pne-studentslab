from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "sequences/U5.fa"

# -- Open and read the file
file_contents = Path(FILENAME).read_text()

list_contents = file_contents.split("\n")
for i in range(1, len(list_contents)):
  print(list_contents[i])

