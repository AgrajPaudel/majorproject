import os
import shutil



def bank_file_maker():
    # User input
    bank_name = input("Enter the bank name: ")

    # Create a folder for the bank if it doesn't exist
    bank_folder = os.path.join(bank_name)
    os.makedirs(bank_folder, exist_ok=True)
    bank_file_list=[]

    # Process and create bank CSV files from templates if they don't exist
    for template_csv in range(1, 6):
        bank_filename = os.path.join(bank_folder, f"{bank_name}data{template_csv}.csv")

        # Check if the bank's CSV file exists
        if not os.path.exists(bank_filename):
            template_filename = f".templates/template{template_csv}.csv"

            # Create a new CSV file as a copy from the template CSV
            shutil.copy(template_filename, bank_filename)
            print(f"CSV file {bank_filename} created.")
        else:
            print(f"CSV file {bank_filename} already exists.")
        bank_file_list.append(bank_filename)

    return bank_file_list


