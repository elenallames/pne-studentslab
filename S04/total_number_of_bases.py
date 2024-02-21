from pathlib import Path

file_name = input("File's name: ")

try:
    file_contents = Path(file_name).read_text()
    lines = file_contents.splitlines()
    body = lines[1:]
    total = 0
    for line in body:
        total += len(line)
    print(f"Total number of bases of the {file_name} file: {total}")
except FileNotFoundError:
    print(f"[ERROR]: file '{file_name}' not found")
except IndexError:
    print(f"[ERROR]: file '{file_name}' is empty")

#another way to do it
#from pathlib import Path
#FILENAME = "sequences/Homo_sapiens_ADA_sequence.fa"
#file_contents = Path(FILENAME).read_text()
#print(file_contents)
#list_contents = file_contents.split("\n")
#list_contents.pop(0)
#print(len("".join(list_contents)))
#############
#index = file_contents.find("\n")
#file_contents = (file_contents[index:]).replace("\n","")
#print(len(file_contents))