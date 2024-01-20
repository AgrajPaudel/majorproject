import pandas as pd
import numpy as np

def merge_row(input_csv_path):
    variables = {
        #remove * -
        # translate & to and
        # space removal?
        "reserves": ["reserves", "reserve and surplus","reserves and surplus"],
        "debenture and bond": ["debenture and bond","debentures and bonds","bond and debenture"],
        "borrowings": ["borrowings"],
        "deposits": ["deposits from customers", "deposits"],
        "income tax liability": ["income tax liability","income tax liabilities"],
        "other liabilities": ["other liabilities","other liabilities and provisions"],
        "total assets": ["total assets"],
        "loan and advancements": ["loan and advancements","loans and advances","net loans and advances"],
        "interest income": ["interest income"],
        "interest expense": ["interest expense"],
        "net interest income": ["net interest income"],
        "net fee and commission income": ["fees, commission and discount","net fee and commission income","net fees and commission income", "fee commission and discount","fees commission and discount","fees, commission and discount"],
        "total operating income": ["total operating income"],
        "staff expenses": ["personnel expenses", "staff expenses"],
        "operating profit": ["operating profit"],
        "non operating income expense": ["non operating income/expense","non operating income/expenses"],
        "profit for the period": ["profit for the period", "net profit/loss","profit/ for the period","profit for the year"],
        "capital fund to rwa": ["capital fund to rwa","capital adequacy","capital fund to risk weighted assets"],
        "non performing loan to total loan": ["non-performing loan to total loan", "npl to total loan","non performing loan to total loan","non performing loans  to total loans"],
        "total loan loss provision to npl": ["total loan loss provision to npl", "total loan loss provision to total npl","total loss loan provision to npl"],
        "cost of fund": ["quarterly average cost of funds","average cost","cost of deposit", "cost of fund","cost of funds","cost of funds lcy deposits","cost of funds lcy"],
        "base rate": ["base rate","average base rate","base rate -average for the quarter"],
        "net interest spread": ["quarterly average interest rate spread","average monthly interest rate spread lcy","net interest spread","interest spread","average interest spread","interest rate spread","lcy interest spread","interest spread lcy"," monthly average interest rate spread"],
        "market share price": ["market share price", "market value per share"],
        "return on equity": ["return on equity"],
        "return on total assets": ["return on total assets", "return on total net assets","return on assets"],
        "credit to deposit ratio": ["cost of funds as of date","credit deposit ratio as per nrb directive","ccd ratio", "c/d ratio", "cd ratio", "credit to deposit ratio","credit deposit ratio","credit/deposit ratio"],
    }

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path, index_col=0)

    # Create a new DataFrame with the same columns as the original DataFrame
    new_df = pd.DataFrame(index=variables.keys(), columns=df.columns)

    # Iterate through the dictionary
    for key, values in variables.items():
        # Copy values for perfectly matching keys
        if key in df.index:
            new_df.loc[key] = df.loc[key]

        # Iterate through datafields for the current key
        for datafield in df.columns:
            # Check if the datafield is empty for the current key
            if pd.isna(new_df.at[key, datafield]) or (
                    isinstance(new_df.at[key, datafield], str) and pd.isna(new_df.at[key, datafield])):
                # Find the unequal value and copy it to the new DataFrame
                for value in values:
                    if value != key and value in df.index:
                        cell_value = df.at[value, datafield]
                        if not pd.Series(cell_value).empty and not pd.Series(cell_value).isna().all():
                            new_df.at[key, datafield] = str(cell_value) if isinstance(cell_value,
                                                                                      np.generic) else cell_value
                            break

    # Save the new DataFrame to the output CSV file
    new_df.to_csv(input_csv_path, index=True)
