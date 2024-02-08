from chardet.universaldetector import UniversalDetector
import os

def detect_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
    detector.close()

    # Return the detected encoding or a default encoding (e.g., 'utf-8')
    return detector.result['encoding'] or 'utf-8'


def convert_to_utf8(file_path, source_encoding):
    with open(file_path, 'r', encoding=source_encoding, errors='replace') as infile:
        content = infile.read()

    with open(file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            source_encoding = detect_encoding(file_path)

            if source_encoding.lower() != 'utf-8':
                print(f"Converting {filename} from {source_encoding} to UTF-8.")
                convert_to_utf8(file_path, source_encoding)
            else:
                print(f"{filename} is already in UTF-8.")