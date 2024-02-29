import os.path
from final_project_single_extraction import extract_text_and_store_csv
import fitz  # PyMuPDF

from final_project_ocr_for_pdf import ocr_for_pdf


def extract_text_from_pdf(pdf_path: str, output_folder: str, filename: str, max_pages: int = 15) -> None:
    # Open the PDF file


    # Check if the input file is a PDF or an image (assuming image files have extensions like jpg, png, etc.)
    _, file_extension = os.path.splitext(pdf_path)

    if file_extension.lower() == '.pdf':
        pdf_document = fitz.open(pdf_path)
        print(pdf_path)

        output_file = os.path.join(output_folder, filename)
        print(output_file)

        # Determine the maximum number of pages to extract
        total_pages = min(pdf_document.page_count, max_pages)

        # Iterate through each page
        with open(output_file, "w", encoding="utf-8") as output_file:
            for page_number in range(total_pages):
                # Get the page
                page = pdf_document[page_number]

                # Extract text from the page
                text = page.get_text()

                # Append text to the output file with a separator
                output_file.write(text)
                output_file.write("\n" + "x" * 80 + "\n")  # Separator between pages

        # Example usage:
        extract_text_and_store_csv(os.path.join(output_folder,filename), output_folder, pdf_path)

        # Close the PDF document
        pdf_document.close()

    elif file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        output_file = os.path.join(output_folder, filename)
        # If it's an image file, use OCR
        ocr_for_pdf(pdf_path=pdf_path, output_folder=output_folder,filename=output_file)

    else:
        print("Unsupported file type. Only PDF and image files (jpg, jpeg, png, gif, bmp) are supported.")



#extract_text_from_pdf(pdf_path='D:/python tesseract/z outp/Q1 2072.pdf',output_folder='D:/python tesseract/z outp/z output',filename='Q1 2072.pdf')