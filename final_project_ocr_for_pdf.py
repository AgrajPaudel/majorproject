import requests
import json
import os
from final_project_ocr_to_csv import extract_from_ocr_to_csv

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine':'2',
               'isTable': True,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

def ocr_for_pdf(pdf_path, output_folder,filename):
    # Call OCR.space API for the given PDF file
    api_key = 'K83942988788957'  # Replace with your actual OCR.space API key
    language = 'eng'  # You can change the language code if needed
    # Perform OCR on the PDF file
    result_json = ocr_space_file(pdf_path, api_key=api_key, language=language)

    # Parse the JSON result
    result_data = json.loads(result_json)

    # Extract text from the parsed JSON result (modify this part based on the actual structure of the OCR result)
    extracted_text = result_data.get('ParsedResults', [{}])[0].get('ParsedText', '')

    # Write the extracted text to the specified text file (test.txt)
    txt_file = filename
    with open(txt_file, 'w', encoding='utf-8') as output_file:
        output_file.write(extracted_text)
    extract_from_ocr_to_csv(pdf_path=pdf_path, output_folder=output_folder, txtfile_name=filename)
    # Write the JSON result to a separate file (test.json)
    #json_file = os.path.join(output_folder, 'test.json')
   # with open(json_file, 'w', encoding='utf-8') as json_output_file:
      #  json.dump(result_data, json_output_file, indent=2)

   # print(f'OCR for PDF done. Text stored in {txt_file}, JSON stored in {json_file}')

