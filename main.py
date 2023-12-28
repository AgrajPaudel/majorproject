from pdf2image import convert_from_path
import os
from shutil import rmtree

# Define the PDF folder containing your PDF files
pdf_folder = 'D:/python tesseract'

# Get a list of PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]

# Loop through each PDF file
for pdf_file in pdf_files:
    # Create a folder with the same name as the PDF (without the .pdf extension)
    folder_name = os.path.splitext(pdf_file)[0]
    folder_path = os.path.join(pdf_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Convert PDF pages to images and save them in the folder
    pages = convert_from_path(os.path.join(pdf_folder, pdf_file))
    for i, page in enumerate(pages):
        image_path = os.path.join(folder_path, f'{i + 1}.png')  # Output image file names as 1.png, 2.png, etc.
        page.save(image_path, 'PNG')

    # Delete the original PDF file
    os.remove(os.path.join(pdf_folder, pdf_file))


