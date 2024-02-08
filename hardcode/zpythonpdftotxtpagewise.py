import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str, output_folder: str, max_pages: int = 15) -> None:
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Determine the maximum number of pages to extract
    total_pages = min(pdf_document.page_count, max_pages)

    # Iterate through each page
    for page_number in range(total_pages):
        # Get the page
        page = pdf_document[page_number]

        # Extract text from the page
        text = page.get_text()

        # Create a text file for each page
        output_file_path = f"{output_folder}/page_{page_number + 1}.txt"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(text)

    # Close the PDF document
    pdf_document.close()
    return text


