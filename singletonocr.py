import os
from PIL import Image
import pytesseract
import cv2

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'  # Replace with your Tesseract executable path

# Specify the folder containing the image files
folder_path = 'D:/python tesseract/'

# Get a list of image file paths in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

# Sort the image file paths for consistent order
image_files.sort()
output_path=os.path.join(folder_path,'z output')



for image_file in image_files:

    image_path = os.path.join(folder_path, image_file)
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to convert to black and white
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # Set pytesseract configuration parameters

    # Use dilation and erosion to enhance text regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    erode = cv2.erode(dilate, kernel, iterations=1)
    text = pytesseract.image_to_string(Image.open(image_path),lang='eng',config='--psm 6')
    filename=image_file.strip('.png')
    output_file=os.path.join(output_path,filename+'.txt')

    with open(output_file, 'w', encoding='utf-8') as output_txt:
        output_txt.write(text)
        output_txt.write("\n" + "-" * 78 + "\n")  # Add a line of dashes to separate the content

print(f'OCR completed. Output saved to: {output_file}')
