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