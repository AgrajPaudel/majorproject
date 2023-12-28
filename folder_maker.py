import os

root_dir = 'Civil Bank Ltd'  # Replace this with your root directory

for foldername, subfolders, files in os.walk(root_dir):
    for filename in files:
        if filename.lower().endswith('.pdf'):
            # Create a folder with the filename (without extension) if it doesn't exist
            folder_path = os.path.join(foldername, os.path.splitext(filename)[0])
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Move the PDF file to the created folder
            file_path = os.path.join(foldername, filename)
            dest_path = os.path.join(folder_path, filename)
            os.rename(file_path, dest_path)
