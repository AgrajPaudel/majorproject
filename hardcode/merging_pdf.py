import PyPDF2
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_watermark_page(watermark_text):
    watermark_page_stream = io.BytesIO()

    watermark_canvas = canvas.Canvas(watermark_page_stream, pagesize=letter)
    watermark_canvas.setFont("Helvetica", 24)  # Adjust the font size
    watermark_canvas.setFillAlpha(0.3)  # Set transparency
    watermark_canvas.setFillGray(0)  # Set color to black

    watermark_canvas.saveState()
    watermark_canvas.rotate(45)  # Rotate the canvas
    watermark_canvas.drawString(200, -200, watermark_text)
    watermark_canvas.restoreState()

    watermark_canvas.save()

    watermark_page_stream.seek(0)
    return PyPDF2.PdfReader(watermark_page_stream).pages[0]

def add_watermark(input_pdf, output_pdf, watermark_text):
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    pdf_writer = PyPDF2.PdfWriter()

    watermark_page = generate_watermark_page(watermark_text)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

if __name__ == "__main__":
    input_folder_path = 'Sunrise Bank Ltd'  # Replace with your input folder path
    output_pdf_path = 'Sunrise Bank Ltd.pdf'  # Replace with your desired output file path

    pdf_files = [os.path.join(input_folder_path, file) for file in os.listdir(input_folder_path) if
                 file.lower().endswith('.pdf')]

    for i, pdf_file in enumerate(pdf_files):
        output_file_path = f'temp_output_{i}.pdf'
        add_watermark(pdf_file, output_file_path, os.path.basename(pdf_file))

    # Merge the PDFs with watermark using PyPDF2
    pdf_merger = PyPDF2.PdfWriter()
    for i in range(len(pdf_files)):
        with open(f'temp_output_{i}.pdf', 'rb') as temp_file:
            pdf_reader = PyPDF2.PdfReader(temp_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_merger.add_page(pdf_reader.pages[page_num])

    # Save the final merged PDF with a larger diagonal, translucent watermark
    with open(output_pdf_path, 'wb') as output_file:
        pdf_merger.write(output_file)

    # Clean up temporary files
    for i in range(len(pdf_files)):
        temp_file_path = f'temp_output_{i}.pdf'
        os.remove(temp_file_path)
