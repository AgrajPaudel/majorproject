import os
from final_project_pdftotxt import extract_text_from_pdf




def process_pdfs_in_directory(directory_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)

        # Check if the file is a PDF
        if os.path.isfile(filepath) and filename.lower().endswith(".pdf"):
            print(f"Processing PDF: {filename}")
            name=filename.strip('.pdf')
            name=name+'.txt'
            print(name)
            # Perform the PDF-to-text conversion
            extract_text_from_pdf(filepath, output_folder,name)



