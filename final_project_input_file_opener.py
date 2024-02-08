import pandas as pd
from final_project_4d_z_score import display_all_quarters_and_banks_for_variable
from final_project_4d_z_score import display_all_banks_for_quarter_and_variable
from final_project_zscore_calculator import calculate_z_score
from final_project_risk_calculator import risk_calculator


def z_score_maker(filename):
    # Read the CSV file
    df = pd.read_csv(filename, index_col=0)

    total_variables = [
        "reserves", "debenture and bond", "borrowings", "deposits", "income tax liability", "other liabilities",
        "total assets", "loan and advancements", "interest income", "interest expense", "net interest income",
        "net fee and commission income", "total operating income", "staff expenses", "operating profit",
        "non operating income expense", "profit for the period", "capital fund to rwa",
        "non performing loan to total loan", "total loan loss provision to npl", "cost of fund", "base rate",
        "net interest spread", "market share price", "return on equity", "return on total assets",
        "credit to deposit ratio", "debt ratio", "interest income to assets ratio", "interest income margin",
        "return on investment", "commission to operating income", "staff expense to income ratio",
        "net profit margin", "income tax portion of operating profit", "loan to deposit ratio"
    ]

    # Define the required variables
    required_variables = [
        "capital fund to rwa", "non performing loan to total loan", "total loan loss provision to npl",
        "cost of fund", "base rate", "net interest spread", "market share price",
        "return on equity", "return on total assets", "credit to deposit ratio", "debt ratio",
        "interest income to assets ratio", "interest income margin", "return on investment",
        "commission to operating income", "staff expense to income ratio", "net profit margin",
        "income tax portion of operating profit", "loan to deposit ratio"
    ]

    # Create a new DataFrame for z-scores
    z_scores_df = pd.DataFrame(index=total_variables, columns=df.columns)

    # Iterate through each column
    for column in df.columns:
        # Iterate through each row and calculate z-scores
        for index, value in df[column].items():
            # Check if the variable is required
            numeric_value = pd.to_numeric(value, errors='coerce')

            if index in total_variables and not pd.isna(numeric_value):
                array_for_all_variables = display_all_quarters_and_banks_for_variable(
                    datafile='D:/python tesseract/3d data/data_cube.csv', variable=index)
                array_for_all_banks_at_a_quarter = display_all_banks_for_quarter_and_variable(
                    datafile='D:/python tesseract/3d data/data_cube.csv', variable=index, quarter=column)
                z_score_for_total = calculate_z_score(array=array_for_all_variables, value=numeric_value)
                z_score_for_quarter = calculate_z_score(array=array_for_all_banks_at_a_quarter, value=numeric_value)

                # Store z-scores in the new DataFrame with 6 decimal places
                z_scores_df.at[index, column] = f"{z_score_for_total:.6f} {z_score_for_quarter:.6f}"

    # Save the z-scores DataFrame to a new CSV file
    z_scores_filename = filename.replace('merged_file.csv', 'z_scores.csv')
    # Save the z-scores DataFrame to a new CSV file with 6 decimal places
    z_scores_df.to_csv(z_scores_filename)
    print(f'Z-scores saved to: {z_scores_filename}')





