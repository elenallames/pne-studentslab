from pathlib import Path

file_name = input("File's name: ")

try:
    file_contents = Path(file_name).read_text()
    print(file_contents)
except FileNotFoundError:
    print(f"[ERROR]: file '{file_name}' not found")

#another way to do it
#from pathlib import Path
#FILENAME = "sequences/Homo_sapiens_RNU6_1155P_sequence.fa"
#file_contents = Path(FILENAME).read_text()
#print(file_contents)