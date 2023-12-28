import os
import shutil

def delete_directory_contents(directory_path):
    try:
        # Iterate over all files and subdirectories in the given directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Check if the item is a file or directory
            if os.path.isfile(item_path):
                # If it's a file, delete it
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                # If it's a directory, delete it recursively
                shutil.rmtree(item_path)

        print(f"Contents of {directory_path} deleted successfully.")
    except Exception as e:
        print(f"Error deleting contents of {directory_path}: {e}")