from pathlib import Path

file_name = input("File's name: ")

try:
    file_contents = Path(file_name).read_text()
    lines = file_contents.splitlines()
    body = lines[1:]
    print(f"Body of the {file_name} file:")
    for line in body:
        print(line)
except FileNotFoundError:
    print(f"[ERROR]: file '{file_name}' not found")
except IndexError:
    print(f"[ERROR]: file '{file_name}' is empty")

#another way to do it
#from pathlib import Path
#FILENAME = "sequences/U5.txt.fa"
#file_contents = Path(FILENAME).read_text()
#header = file_contents.find("\n")
#body = file_contents[header:]
#print(body)

#list_contents = file_contents.split("\n")
#for i in range(1, len(list_contents)
#   print(list_contents[i])