import os
import cv2
from PIL import Image
import pytesseract

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'  # Replace with your Tesseract executable path

# Specify the parent folder containing the subfolders with images
parent_folder = 'sbi nepal bank'

# Get a list of subfolders in the parent folder
subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

# Loop through each subfolder
for subfolder in subfolders:
    subfolder_path = os.path.join(parent_folder, subfolder)

    # Get a list of image file paths in the subfolder
    image_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort the image file paths numerically
    image_files.sort(key=lambda x: int(x.split('.')[0]))

    # Output file path for the subfolder
    output_file = os.path.join(subfolder_path, f'{subfolder}.txt')

    with open(output_file, 'w', encoding='utf-8') as output_txt:
        for image_file in image_files:
            image_path = os.path.join(subfolder_path, image_file)
            # Read the image using OpenCV for preprocessing
            img = cv2.imread(image_path)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to convert to black and white
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            # Use dilation and erosion to enhance text regions
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            dilate = cv2.dilate(thresh, kernel, iterations=1)
            erode = cv2.erode(dilate, kernel, iterations=1)
            text = pytesseract.image_to_string(Image.open(image_path),lang='eng',config='--psm 6')
            output_txt.write(text)
            output_txt.write("\n" + "-" * 78 + "\n")  # Add a line of dashes to separate the content

    print(f'OCR completed for {subfolder}. Output saved to: {output_file}')
