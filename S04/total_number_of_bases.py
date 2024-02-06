from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "sequences/ADA.fa"

# -- Open and read the file
file_contents = Path(FILENAME).read_text()



total_number_of_bases = len(list_contents)
print(total_number_of_bases)
