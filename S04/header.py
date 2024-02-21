from pathlib import Path

file_name = input("File's name: ")

try:
    file_contents = Path(file_name).read_text()
    lines = file_contents.splitlines()
    head = lines[0]
    print(head)
except FileNotFoundError:
    print(f"[ERROR]: file '{file_name}' not found")
except IndexError:
    print(f"[ERROR]: file '{file_name}' is empty")

#another way to do it
#from pathlib import Path
#FILENAME = "sequences/RNU6_269P.fa"
#file_contents = Path(FILENAME).read_text()
#list_contents = file_contents.split("\n")
#print(list_contents[0])