import os

from final_project_pdftotxt import extract_text_from_pdf
from final_project_delete_directory_content import delete_directory_contents
from final_project_csv_merger import combine_csv_files
from final_project_remove_percent_and_comma import  clean_csv_files_in_folder
from final_project_fill_the_gaps import  add_and_store_in_folder
#from final_project_calculator import calculate_values_and_update_csv

def single_pdf_extraction(file_path,access_token_folder,filename):
    delete_directory_contents(access_token_folder)
    # Example usage:
    extract_text_from_pdf(file_path,access_token_folder,filename)
    clean_csv_files_in_folder(folder_path=access_token_folder)
    add_and_store_in_folder(access_token_folder)
    #file_path=os.path.join(access_token_folder,filename)
    #print(file_path)
    #file_path, _ = os.path.splitext(file_path)
    #print(file_path)
    #file_path=file_path+'_output.csv'
    # Example usage:
    #calculate_values_and_update_csv(file_path)


def multiple_pdf_extraction(input_folder, access_token_folder, merged_csv_name):
    delete_directory_contents(access_token_folder)

    # Get a list of all files (PDFs or images) in the input_folder
    files_list = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file))]

    for file_name in files_list:
        file_path = os.path.join(input_folder, file_name)

        # Extract filename without extension
        filename_without_extension = os.path.splitext(file_name)[0]

        # Call extract_text_from_pdf for each file
        extract_text_from_pdf(file_path, access_token_folder, f"{filename_without_extension}.txt")

    combine_csv_files(input_folder=access_token_folder,merged_csv_name=merged_csv_name)
    clean_csv_files_in_folder(folder_path=access_token_folder)
    add_and_store_in_folder(access_token_folder)


