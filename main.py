import sys
from function_opener import multiple_pdf_extraction
from final_project_input_file_opener import z_score_maker
from final_project_extract_data_from_input import (
    display_all_quarters_for_variable,
    get_values_for_quarter
)
from final_project_interpolated import interpolate_nan
from final_project_1_extract_unit_data import (
    display_all_banks_for_quarter_and_variable,
    display_bank_quarter_data,
    display_all_quarters_for_bank_and_variable
)
from final_project_outlier_finding import get_variable_info
from final_project_outlier_finding_from_input import get_variable_info as get_variable_info_from_input
from final_project_risk_analysis import risk_analysis,risk_analysis_from_inputs
from final_project_knn import get_column_data
from final_project_extract_rows import get_csv_row_headers
import os
import json

path = 'D:/python tesseract'
datafile = 'D:/python tesseract/3d data/data_cube.csv'



def extract_value(json_data, key):
    return json_data.get(key, None)


# Function to create folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

#code to extract row titles from new file
def extract_row_index(access_token,filename):
    folder = os.path.join(path, access_token)
    output_folder = os.path.join(folder, 'z output')
    newfile_path = os.path.join(os.path.join(folder, 'z output'), filename)

    try:
        values = get_csv_row_headers(file_path=newfile_path)
        result_file_path = os.path.join(output_folder, 'row_headers.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values
    except Exception as e:
        error_message = f'Error in extract_row_index: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'row_headers.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})



# Code to enter and work on files
def work_on_input(access_token):
    # Create input folder if not present
    input_folder = os.path.join(path, access_token)
    create_folder_if_not_exists(input_folder)

    # Create output folder if not present
    output_folder = os.path.join(input_folder, 'z output')
    create_folder_if_not_exists(output_folder)

    try:
        # Extraction + merging csv file
        multiple_pdf_extraction(input_folder=input_folder, access_token_folder=output_folder,
                                merged_csv_name='merged_file.csv')

        # Calculating z score
        z_score_maker(filename=os.path.join(output_folder, 'merged_file.csv'))

        values= 'Process done.'
        result_file_path = os.path.join(output_folder, 'input_work.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values

    except Exception as e:
        error_message = f'Error in work_on_input: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'input_work.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


# Code to extract data from new files
def quarter_extraction_from_newfile(access_token, quarter, filename):
    folder = os.path.join(path, access_token)
    output_folder = os.path.join(folder, 'z output')
    newfile_path = os.path.join(os.path.join(folder, 'z output'), filename)

    try:
        values = get_values_for_quarter(quarter=quarter, datafile=newfile_path)
        result_file_path = os.path.join(output_folder, 'quarter_from_input.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values
    except Exception as e:
        error_message = f'Error in extract_quarter_from_newfile: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'quarter_from_input.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def variable_extraction_from_newfile(access_token, variable, filename):
    folder = os.path.join(path, access_token)
    output_folder = os.path.join(folder, 'z output')
    newfile_path = os.path.join(os.path.join(folder, 'z output'), filename)

    try:
        values = display_all_quarters_for_variable(variable=variable, datafile=newfile_path)
        result_file_path = os.path.join(output_folder, 'variable_from_input.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values
    except Exception as e:
        error_message = f'Error in variable_from_new_file: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'variable_from_input.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def bank_and_variable_extraction_from_oldfiles(access_token,bank, variable):
    input_folder = os.path.join(path, access_token)
    output_folder = os.path.join(input_folder, 'z output')
    try:
        value = display_all_quarters_for_bank_and_variable(variable=variable, bank=bank, datafile=datafile)
        values=interpolate_nan(value)
        print(values)
        result_file_path = os.path.join(output_folder, 'bank_and_variable_existing.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values
    except Exception as e:
        error_message = f'Error in bank_and_variable_extraction_from_oldfiles: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'bank_and_variable_existing.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def variable_and_quarter_extraction_from_oldfiles(access_token,quarter, variable):
    input_folder = os.path.join(path, access_token)
    output_folder = os.path.join(input_folder, 'z output')
    try:
        values = display_all_banks_for_quarter_and_variable(quarter=quarter, variable=variable, datafile=datafile)
        result_file_path = os.path.join(output_folder, 'variable_and_quarter_existing.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values
    except Exception as e:
        error_message = f'Error in variable_and_quarter_extraction_from_oldfiles: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'variable_and_quarter_existing.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def bank_and_quarter_extraction_from_oldfiles(access_token,bank, quarter):
    input_folder = os.path.join(path, access_token)
    output_folder = os.path.join(input_folder, 'z output')
    try:
        values = display_bank_quarter_data(quarter=quarter, bank=bank, datafile=datafile)
        result_file_path = os.path.join(output_folder, 'bank_and_quarter_existing.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)
        return values
    except Exception as e:
        error_message = f'Error in bank_and_quarter_extraction_from_oldfiles: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'bank_and_quarter_existing.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})

# calculations
def outlier_from_existing(access_token,quarter, bank, filepath):
    input_folder = os.path.join(path, access_token)
    output_folder = os.path.join(input_folder, 'z output')
    try:
        values = get_variable_info(quarter=quarter, bank=bank, datafile=filepath)
        result_file_path=os.path.join(output_folder,'outlier_from_existing.json')
        with open(result_file_path,'w') as result_file:
            json.dump(values,result_file)
        return values
    except Exception as e:
        error_message = f'Error in outlier_from_existing: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'outlier_from_existing.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def outlier_from_input(quarter, access_token):
    input_folder = os.path.join(path, access_token)
    output_folder = os.path.join(input_folder, 'z output')

    try:
        values = get_variable_info_from_input(quarter=quarter, datafile=os.path.join(output_folder, 'z_scores.csv'))

        # Save the result as a JSON file
        result_file_path = os.path.join(output_folder, 'outlier_from_input.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)

        return values
    except Exception as e:
        error_message = f'Error in outlier_from_input: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'outlier_from_input.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def risk_analysis_existing(quarter, bank, filepath, access_token):
    try:
        values = risk_analysis(datafile=filepath, quarter=quarter, bank=bank)
        payload = {f'{i + 1}th risk': value for i, value in enumerate(values)}

        # Save the result as a JSON file
        result_file_path = os.path.join(path, access_token, 'z output', 'risk_analysis_existing.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(payload, result_file)

        return json.dumps(payload)
    except Exception as e:
        error_message = f'Error in risk_analysis_existing: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(path, access_token, 'z output', 'risk_analysis_existing.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})


def risk_analysis_from_input(quarter, filepath, access_token):
    try:
        values = risk_analysis_from_inputs(datafile=filepath, quarter=quarter)
        payload = {f'{i + 1}th risk': value for i, value in enumerate(values)}

        # Save the result as a JSON file
        result_file_path = os.path.join(path, access_token, 'z output', 'risk_analysis_input.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(payload, result_file)

        return json.dumps(payload)
    except Exception as e:
        error_message = f'Error in risk_analysis_input: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(path, access_token, 'z output', 'risk_analysis_input.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})

# knn
def knn_output(access_token):
    input_folder = os.path.join(path, access_token)
    output_folder = os.path.join(input_folder, 'z output')

    try:
        values = get_column_data(datafile=datafile, filename=os.path.join(output_folder, 'merged_file.csv'))

        # Save the result as a JSON file
        result_file_path = os.path.join(output_folder, 'knn_output.json')
        with open(result_file_path, 'w') as result_file:
            json.dump(values, result_file)

        return values
    except Exception as e:
        error_message = f'Error in knn output: {str(e)}'

        # Save the error message as a JSON file
        error_file_path = os.path.join(output_folder, 'knn_output.json')
        with open(error_file_path, 'w') as error_file:
            json.dump({'error': error_message}, error_file)

        return json.dumps({'error': error_message})

if __name__ == "__main__":
    try:
        # Retrieve arguments
        json_input = json.loads(sys.argv[1])
        values=None
        # Extract values based on keys
        access_token = extract_value(json_input, 'access_token')
        function_name = extract_value(json_input, 'functionname')

        # Create a dictionary to store arguments
        args_dict = {'access_token': access_token}

        # Populate the args_dict based on the function's expected arguments
        if function_name == 'work_on_input':

            try:
                values = work_on_input(args_dict['access_token'])


            except Exception as e:
                values = str(f'Error: {str(e)}')

        elif function_name == 'extract_row_index':
            args_dict['filename'] = extract_value(json_input,'filename')
            try:
                values=extract_row_index(access_token=access_token,filename=args_dict['filename'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'quarter_extraction_from_newfile':
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            args_dict['filename'] = extract_value(json_input, 'filename')
            try:
                values=quarter_extraction_from_newfile(access_token=access_token,quarter=args_dict['quarter'],filename=args_dict['filename'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'variable_extraction_from_newfile':
            args_dict['variable'] = extract_value(json_input, 'variable')
            args_dict['filename'] = extract_value(json_input, 'filename')
            try:
                values=variable_extraction_from_newfile(access_token=access_token,variable=args_dict['variable'],filename=args_dict['filename'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')

        elif function_name == 'bank_and_variable_extraction_from_oldfiles':
            args_dict['bank'] = extract_value(json_input, 'bank')
            args_dict['variable'] = extract_value(json_input, 'variable')
            try:
                values=bank_and_variable_extraction_from_oldfiles(access_token=access_token,variable=args_dict['variable'],bank=args_dict['bank'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'variable_and_quarter_extraction_from_oldfiles':
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            args_dict['variable'] = extract_value(json_input, 'variable')
            try:
                values=variable_and_quarter_extraction_from_oldfiles(access_token=access_token,quarter=args_dict['quarter'],variable=args_dict['variable'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'bank_and_quarter_extraction_from_oldfiles':
            args_dict['bank'] = extract_value(json_input, 'bank')
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            try:
                values=bank_and_quarter_extraction_from_oldfiles(access_token=access_token,quarter=args_dict['quarter'],bank=args_dict['bank'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'outlier_from_existing':
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            args_dict['bank'] = extract_value(json_input, 'bank')
            args_dict['filepath'] = extract_value(json_input, 'filepath')
            try:
                values=outlier_from_existing(access_token=access_token,quarter=args_dict['quarter'],bank=args_dict['bank'],filepath=args_dict['filepath'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'outlier_from_input':
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            try:
                values=outlier_from_input(access_token=access_token,quarter=args_dict['quarter'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
            #done
        elif function_name == 'risk_analysis_existing':
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            args_dict['bank'] = extract_value(json_input, 'bank')
            args_dict['filepath'] = extract_value(json_input, 'filepath')

            try:
                values=risk_analysis_existing(access_token=access_token,quarter=args_dict['quarter'],bank=args_dict['bank'],filepath=args_dict['filepath'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')

        elif function_name == 'risk_analysis_input':
            args_dict['quarter'] = extract_value(json_input, 'quarter')
            args_dict['filepath'] = extract_value(json_input, 'filepath')

            try:
                values=risk_analysis_from_input(access_token=access_token,quarter=args_dict['quarter'],filepath=args_dict['filepath'])


            except Exception as e:
                values=  str(f'Error: {str(e)}')
        elif function_name == 'knn_output':
            try:
                values = knn_output(access_token=access_token)


            except Exception as e:
                values = str(f'Error: {str(e)}')
        else:
            print(f'Error: Unknown function name - {function_name}')
            sys.exit(1)

    except Exception as e:

        values=str(f'Error: {str(e)}')

