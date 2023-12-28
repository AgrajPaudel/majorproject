import pandas as pd

# List of CSV files
csv_files = ['LaxmiBankData1.csv', 'LaxmiBankData2.csv', 'LaxmiBankData3.csv','LaxmiBankData4.csv','LaxmiBankData5.csv']  # Add your file names

# Create an Excel writer object
excel_writer = pd.ExcelWriter('output_file.xlsx', engine='xlsxwriter')

# Loop through each CSV file and write to a separate worksheet
for csv_file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract the file name (excluding the extension) to use as the worksheet name
    sheet_name = csv_file.split('.')[0]

    # Write the DataFrame to the Excel file
    df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

# Save the Excel file
excel_writer._save()
