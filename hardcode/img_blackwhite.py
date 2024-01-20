from PIL import Image

# Specify the path to the input image
input_image_path = 'D:/python tesseract/Nepal Investment Bank/Q1 2073/1.png'

# Specify the path to save the black and white image
output_image_path = 'D:/python tesseract/Nepal Investment Bank/Q1 2073/11.png'

# Open the input image
img = Image.open(input_image_path)

# Convert the image to black and white
img_bw = img.convert('L')  # 'L' mode represents 8-bit pixels, black and white

# Save the black and white image
img_bw.save(output_image_path)

# Optionally, show the images
img.show()
img_bw.show()
