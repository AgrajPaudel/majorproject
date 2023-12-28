import os
from pdftotxt import txtmaker
from file_operations import bank_file_maker
from checkingfromcsvtotxt import  checker
from checkingoverflow import variable as v
import time





bankfile_list=bank_file_maker()

# Specify the parent folder containing the subfolders with images
parent_folder = 'Civil Bank Ltd'

# Get a list of subfolders in the parent folder
subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

# Loop through each subfolder
for subfolder in subfolders:
    subfolder_path = os.path.join(parent_folder, subfolder)

    # Get a list of pdf file paths in the subfolder
    pdf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.pdf'))]
    img_files=[f for f in os.listdir(subfolder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if(v<=2):





        for pdf_file in pdf_files:
            pdf_path = os.path.join(subfolder_path, pdf_file)

            print(pdf_file) #name of file
            print(subfolder_path)   #before file
            print(pdf_path)  #fullpath
            quarter = pdf_file.strip('.pdf')
            output_files = txtmaker(pdf_path,subfolder_path,pdf_file)
            print(output_files)
            time.sleep(3)
            x=checker(bankfile_list,output_files,quarter,subfolder_path,pdf_file)


      #   for img_file in img_files:
       #     quarter = img_file.strip('.png')
        #    print(quarter)
        #    quarter =img_file.strip('.jpg')
        #    print(quarter)
         #   img_path=os.path.join(subfolder_path, img_file)
         #   txtfile = img_file.strip('.png')
         #   print(txtfile)
        #    txtfile=img_file.strip('.jpg')
          #  print(txtfile)
         #   output_file = os.path.join(img_path, f'{txtfile}.txt')
          #  with open(output_file, 'w', encoding='utf-8') as output_txt:
          #      img = cv2.imread(img_path)

          #      # Convert to grayscale
           #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
           #     # Apply thresholding to convert to black and white
           #     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#
           #     # Use dilation and erosion to enhance text regions
          #      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
          #      dilate = cv2.dilate(thresh, kernel, iterations=1)
         #       erode = cv2.erode(dilate, kernel, iterations=1)
            #    text = pytesseract.image_to_string(Image.open(img_path), lang='eng', config='--psm 6')
         #       output_txt.write(text)
           #     output_txt.write("\n" + "-" * 78 + "\n")  # Add a line of dashes to separate the content
#
          #  outputfiles = txt_splitter(output_file, img_path, f'{txtfile}.txt')
          #  x = checker(bankfile_list, outputfiles, quarter, subfolder_path, img_file)



    else:
        print("overflow")



