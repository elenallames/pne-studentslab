from pathlib import Path

file_name = input("File's name: ")

try:
    file_contents = Path(file_name).read_text()
    print(file_contents)
except FileNotFoundError:
    print(f"[ERROR]: file '{file_name}' not found")

