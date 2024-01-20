import os

def txt_splitter(input_txt_file_path,subfolder_path,filename):
    textfile_list = []

    # Define the 2D list of conditions
    conditions = [
        ["Ratios", "NRB", "Directive"],
        ["Condensed", "Statement", "cash", "flows"],
        ["Condensed", "Statement", "Profit", "Loss"]
    ]

    # Function to check if all words in a condition exist in a line
    def should_create_new_file(line, conditions_met):
        line = line.lower()  # Convert the line to lowercase
        for condition in conditions:
            if all(word.lower() in line for word in condition):
                # If the condition is met and not already in conditions_met, return True
                if tuple(condition) not in conditions_met:
                    conditions_met.add(tuple(condition))
                    return True
        return False

    # Create the initial text file
    output_dir = subfolder_path
    stripped_filename=filename.strip('.txt')
    current_text_file = open(os.path.join(output_dir, stripped_filename +str(' 1')+'.txt'), 'w', encoding='utf-8')
    textfile_list.append(os.path.join(output_dir, stripped_filename+str(' 1')+'.txt'))
    print(textfile_list)

    # Set to keep track of conditions met
    conditions_met = set()

    # Open the input text file and process the content
    with open(input_txt_file_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
        index=2
        for line in lines:
            # Check if the line is not empty or doesn't consist of only spaces
            if line.strip():
                # Check if conditions are met to create a new text file
                if should_create_new_file(line, conditions_met):
                    # Close the current text file
                    current_text_file.close()
                    # Create a new text file with a unique name
                    output_files = os.listdir(output_dir)
                    strippedfilename=filename.strip('.txt')
                    new_file_name = strippedfilename +f' {str(index)}.txt'
                    current_text_file = open(os.path.join(output_dir, new_file_name), 'w', encoding='utf-8')
                    index=index+1
                    textfile_list.append(os.path.join(output_dir, new_file_name))
                # Write the line to the current text file
                current_text_file.write(line)

    # Close the current text file
    current_text_file.close()
    print('Text files created based on specified conditions.')

    return textfile_list

