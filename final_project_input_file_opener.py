import pandas as pd
from final_project_4d_z_score import display_all_quarters_and_banks_for_variable
from final_project_4d_z_score import display_all_banks_for_quarter_and_variable
from final_project_zscore_calculator import calculate_z_score
from final_project_risk_calculator import  risk_calculator

def print_column_data(filename):
    # Read the CSV file
    df = pd.read_csv(filename, index_col=0)

    # Define the required variables
    required_variables = [
        "capital fund to rwa",
        "non performing loan to total loan",
        "total loan loss provision to npl",
        "cost of fund",
        "base rate",
        "net interest spread",
        "market share price",
        "return on equity",
        "return on total assets",
        "credit to deposit ratio",
        "debt ratio",
        "interest income to assets ratio",
        "interest income margin",
        "return on investment",
        "commission to operating income",
        "staff expense to income ratio",
        "net profit margin",
        "income tax portion of operating profit",
        "loan to deposit ratio"
    ]

    # Iterate through each column
    for column in df.columns:
        # Print the column header
        print(f"Column: {column}")

        # Store z-scores for the current column
        z_scores = []

        # Iterate through each row and print variable and value
        for index, value in df[column].items():
            # Check if the variable is required
            if index in required_variables:
                # Convert value to numeric, if possible
                numeric_value = pd.to_numeric(value, errors='coerce')

                # Only proceed if the numeric conversion was successful
                if not pd.isna(numeric_value):
                    array_for_all_variables = display_all_quarters_and_banks_for_variable(
                        datafile='D:/python tesseract/3d data/data_cube.csv', variable=index)
                    array_for_all_banks_at_a_quarter = display_all_banks_for_quarter_and_variable(
                        datafile='D:/python tesseract/3d data/data_cube.csv', variable=index, quarter=column)
                    z_score_for_total = calculate_z_score(array=array_for_all_variables, value=numeric_value)
                    z_score_for_quarter = calculate_z_score(array=array_for_all_banks_at_a_quarter, value=numeric_value)

                    # Store z-scores for the current variable
                    z_scores.append([index, z_score_for_total, z_score_for_quarter])


                else:
                    # Append variable name and two NaN values to z_scores
                    z_scores.append([index, float('nan'), float('nan')])



        # Example: Call the risk_calculator function with z-scores
        first_risk = risk_calculator(
            capital_fund_to_rwa=z_scores[0][1],
            non_performing_loan_to_total_loan=z_scores[1][1],
            total_loan_loss_provision_to_npl=z_scores[2][1],
            cost_of_fund=z_scores[3][1],
            net_interest_spread=z_scores[4][1],
            base_rate=z_scores[5][1],
            return_on_total_assets=z_scores[6][1],
            return_on_equity=z_scores[7][1],
            credit_to_deposit_ratio=z_scores[8][1],
            debt_ratio=z_scores[9][1],
            income_tax_portion_of_operating_profit=z_scores[10][1],
            interest_income_to_assets_ratio=z_scores[11][1],
            interest_income_margin=z_scores[12][1],
            return_on_investment=z_scores[13][1],
            commission_to_operating_income=z_scores[14][1],
            net_profit_margin=z_scores[15][1],
            staff_expense_to_income_ratio=z_scores[16][1],
            loan_to_deposit_ratio=z_scores[17][1]  # This should take entry[1] if index is "loan to deposit ratio"
        )

        # Example: Call the risk_calculator function with z-scores for the second risk
        second_risk = risk_calculator(
            capital_fund_to_rwa=z_scores[0][2],
            non_performing_loan_to_total_loan=z_scores[1][2],
            total_loan_loss_provision_to_npl=z_scores[2][2],
            cost_of_fund=z_scores[3][2],
            net_interest_spread=z_scores[4][2],
            base_rate=z_scores[5][2],
            return_on_total_assets=z_scores[6][2],
            return_on_equity=z_scores[7][2],
            credit_to_deposit_ratio=z_scores[8][2],
            debt_ratio=z_scores[9][2],
            income_tax_portion_of_operating_profit=z_scores[10][2],
            interest_income_to_assets_ratio=z_scores[11][2],
            interest_income_margin=z_scores[12][2],
            return_on_investment=z_scores[13][2],
            commission_to_operating_income=z_scores[14][2],
            net_profit_margin=z_scores[15][2],
            staff_expense_to_income_ratio=z_scores[16][2],
            loan_to_deposit_ratio=z_scores[17][2]  # This should take entry[2] if index is "loan to deposit ratio"
        )
        print(f'first risk= {first_risk} and second risk= {second_risk}')


# Example usage
csv_filename = 'D:/python tesseract/z output/merged_file.csv'
print_column_data(csv_filename)
