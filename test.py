if __name__ == "__main__":
    # Retrieve arguments
    access_token = sys.argv[1]
    function_name = sys.argv[2]

    # Additional arguments based on function
    additional_args = sys.argv[3:]

    # Create a dictionary to store arguments
    args_dict = {}

    # Populate the args_dict based on the function's expected arguments
    if function_name == 'work_on_input':
        args_dict['access_token'] = access_token
    elif function_name == 'quarter_extraction_from_newfile':
        args_dict['access_token'], args_dict['quarter'], args_dict['filename'] = access_token, *additional_args
    elif function_name == 'variable_extraction_from_newfile':
        args_dict['access_token'], args_dict['variable'], args_dict['filename'] = access_token, *additional_args
    elif function_name == 'bank_and_variable_extraction_from_oldfiles':
        args_dict['bank'], args_dict['variable'] = additional_args
    elif function_name == 'variable_and_quarter_extraction_from_oldfiles':
        args_dict['quarter'], args_dict['variable'] = additional_args
    elif function_name == 'bank_and_quarter_extraction_from_oldfiles':
        args_dict['bank'], args_dict['quarter'] = additional_args
    elif function_name == 'outlier_from_existing':
        args_dict['quarter'], args_dict['bank'], args_dict['filepath'] = additional_args
    elif function_name == 'outlier_from_input':
        args_dict['quarter'] = additional_args[0]
    elif function_name == 'risk_analysis_existing':
        args_dict['quarter'], args_dict['bank'], args_dict['filepath'] = additional_args
        args_dict['quarter'] = args_dict.pop('quarters', args_dict['quarter'])
        args_dict['bank'] = args_dict.pop('banks', args_dict['bank'])
    elif function_name == 'knn_output':
        args_dict['access_token'] = access_token
    else:
        print(f'Error: Unknown function name - {function_name}')
        sys.exit(1)

    # Call the appropriate function with the args_dict
    try:
        result = globals()[function_name](**args_dict)
        print(result)
    except Exception as e:
        print(f'Error: {str(e)}')
