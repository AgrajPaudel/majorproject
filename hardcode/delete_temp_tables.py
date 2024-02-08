import os

def delete_files(file_list):
    for file_path in file_list:
        try:
            file_path=os.path.join('', file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")


