import pandas as pd
import os
# Load the CSV file





def count_stats(file_path):
    try:
        data = pd.read_csv(file_path)
        total_fields = data.size
        empty_fields = data.isnull().sum().sum() + data[data.eq('').any(axis=1)].sum().sum()
        outliers = data.astype(str).apply(lambda x: x.str.contains(r'\*', na=False)).sum().sum()
        correct_data = total_fields - empty_fields - outliers

        print("Total Number of Data Fields:", total_fields)
        print("Empty Fields:", empty_fields)
        print("Outliers:", outliers)
        print("Correct Data Fields:", correct_data)
        if(total_fields!=0):
            percentage_of_correct_data=correct_data/total_fields
            possible_percentage=(correct_data+outliers)/total_fields
            print("Correct data percentage: ", percentage_of_correct_data)
            print('Possible correct percent', possible_percentage)
            x=[percentage_of_correct_data,possible_percentage]
        else:
            x=[1,1]
        return x
    except pd.errors.EmptyDataError:
        print("The provided CSV file is empty or doesn't contain any data.")
        x=[0,0]
        return x




parent_folder = 'z output'

# Get a list of subfolders in the parent folder
subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
sum=0
possible_sum=0
num=0
# Loop through each subfolder
for subfolder in subfolders:
    subfolder_path = os.path.join(parent_folder, subfolder)

    # Get a list of pdf file paths in the subfolder
    pdf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.csv'))]
    for pdf_file in pdf_files:
        num = num + 1
        pdf_path = os.path.join(subfolder_path, pdf_file)
        x=pdf_file.strip('.csv')
        print(pdf_file)  # name of file
        print(subfolder_path)  # before file
        print(pdf_path)# fullpath
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
        avg=count_stats(pdf_path)
        print(avg[0])
        sum=sum+avg[0]
        possible_sum=possible_sum+avg[1]

        print('work done in : '+pdf_path)

average=sum/num
possible_average=possible_sum/num
print('Avg correct percentage=', average)
print('Avg possible correct percentage=', possible_average)





