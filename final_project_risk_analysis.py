import pandas as pd
from final_project_risk_calculator import risk_calculator

max=[0.953690214839989,0.8820812056064548,0.8623360470815973]
min=[-1.0000000000000002,-0.8978659288706474,-0.9907139822450888]


def separate_string(input_string):
    # Split the string into words using space as the delimiter
    words=[]

    # Check if there's only one word
    if str(input_string)=='nan':
        words.append(input_string)
        # Repeat the word three times
        words *= 3
    else:
        words = input_string.split()
    return words

def separate_string_input(input_string):
    # Split the string into words using space as the delimiter
    words=[]

    # Check if there's only one word
    if str(input_string)=='nan':
        words.append(input_string)
        # Repeat the word three times
        words *= 2
    else:
        words = input_string.split()
    return words



def extract_z_scores(variable_and_z_scores, variable_name):
    for variable, z_scores in variable_and_z_scores:
        if variable == variable_name:
            return z_scores


def display_input_quarter_data(datafile, quarter):
    # Read the data CSV file
    df = pd.read_csv(datafile, index_col=0)

    try:
        # Use loc to access data for the specified quarter
        result = df[quarter]
        variable_names = result.index.tolist()

        # Extract values from the result Series
        values = result.values.tolist()

        # Create a 2D array
        variable_data = list(zip(variable_names, values))

        return variable_data

    except KeyError:
        print(f"Data not found for quarter: {quarter}")



def display_bank_quarter_data(datafile, bank, quarter):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=[0, 'Bank'])

    try:
        # Use loc to access data for the specified bank and quarter
        result = df.loc[(slice(None), bank), quarter]
        variable_names = result.index.get_level_values(0).tolist()

        # Extract values from the result DataFrame
        values = result.values.flatten().tolist()

        # Create a 2D array
        variable_data = list(zip(variable_names, values))


        return variable_data

    except KeyError:
        print(f"Data not found for bank: {bank} and quarter: {quarter}")

def risk_analysis(datafile, quarter, bank):
    variable_and_z_scores=display_bank_quarter_data(datafile=datafile, quarter=quarter, bank=bank)






    extraction = extract_z_scores(variable_and_z_scores, 'non performing loan to total loan')
    non_performing_loan_to_total_loan = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'total loan loss provision to npl')
    total_loan_loss_provision_to_npl = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'cost of fund')
    cost_of_fund = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'base rate')
    base_rate = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'net interest spread')
    net_interest_spread = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'return on equity')
    return_on_equity = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'return on total assets')
    return_on_total_assets = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'credit to deposit ratio')
    credit_to_deposit_ratio = separate_string(extraction)





    extraction = extract_z_scores(variable_and_z_scores, 'capital fund to rwa')
    capital_fund_to_rwa = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'loan to deposit ratio')
    loan_to_deposit_ratio = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'income tax portion of operating profit')
    income_tax_portion_of_operating_profit = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'net profit margin')
    net_profit_margin = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'staff expense to income ratio')
    staff_expense_to_income_ratio = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'commission to operating income')
    commission_to_operating_income = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'return on investment')
    return_on_investment = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'interest income margin')
    interest_income_margin = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'interest income to assets ratio')
    interest_income_to_assets_ratio = separate_string(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'debt ratio')
    debt_ratio = separate_string(extraction)

    risk_array=[]
    i=0
    while i<3:

        risk=risk_calculator(capital_fund_to_rwa=capital_fund_to_rwa[i],
                             non_performing_loan_to_total_loan=non_performing_loan_to_total_loan[i],
                             total_loan_loss_provision_to_npl=total_loan_loss_provision_to_npl[i],
                             cost_of_fund=cost_of_fund[i],
                             net_interest_spread=net_interest_spread[i],
                             base_rate=base_rate[i],
                             return_on_total_assets=return_on_total_assets[i],
                             return_on_equity=return_on_equity[i],
                             credit_to_deposit_ratio=credit_to_deposit_ratio[i],
                             debt_ratio=debt_ratio[i],
                             income_tax_portion_of_operating_profit=income_tax_portion_of_operating_profit[i],
                             interest_income_to_assets_ratio=interest_income_to_assets_ratio[i],
                             interest_income_margin=interest_income_margin[i],
                             return_on_investment=return_on_investment[i],
                             commission_to_operating_income=commission_to_operating_income[i],
                             net_profit_margin=net_profit_margin[i],
                             staff_expense_to_income_ratio=staff_expense_to_income_ratio[i],
                             loan_to_deposit_ratio=loan_to_deposit_ratio[i],
                             )

        risk = [round(num) for num in risk]
        risk_array.append(risk)
        i=i+1

    return risk_array


def risk_analysis_from_inputs(datafile, quarter):

    variable_and_z_scores=display_input_quarter_data(datafile=datafile, quarter=quarter)






    extraction = extract_z_scores(variable_and_z_scores, 'non performing loan to total loan')
    non_performing_loan_to_total_loan = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'total loan loss provision to npl')
    total_loan_loss_provision_to_npl = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'cost of fund')
    cost_of_fund = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'base rate')
    base_rate = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'net interest spread')
    net_interest_spread = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'return on equity')
    return_on_equity = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'return on total assets')
    return_on_total_assets = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'credit to deposit ratio')
    credit_to_deposit_ratio = separate_string_input(extraction)





    extraction = extract_z_scores(variable_and_z_scores, 'capital fund to rwa')
    capital_fund_to_rwa = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'loan to deposit ratio')
    loan_to_deposit_ratio = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'income tax portion of operating profit')
    income_tax_portion_of_operating_profit = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'net profit margin')
    net_profit_margin = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'staff expense to income ratio')
    staff_expense_to_income_ratio = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'commission to operating income')
    commission_to_operating_income = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'return on investment')
    return_on_investment = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'interest income margin')
    interest_income_margin = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'interest income to assets ratio')
    interest_income_to_assets_ratio = separate_string_input(extraction)


    extraction = extract_z_scores(variable_and_z_scores, 'debt ratio')
    debt_ratio = separate_string_input(extraction)

    risk_array=[]
    i=0
    while i<2:

        risk=risk_calculator(capital_fund_to_rwa=capital_fund_to_rwa[i],
                             non_performing_loan_to_total_loan=non_performing_loan_to_total_loan[i],
                             total_loan_loss_provision_to_npl=total_loan_loss_provision_to_npl[i],
                             cost_of_fund=cost_of_fund[i],
                             net_interest_spread=net_interest_spread[i],
                             base_rate=base_rate[i],
                             return_on_total_assets=return_on_total_assets[i],
                             return_on_equity=return_on_equity[i],
                             credit_to_deposit_ratio=credit_to_deposit_ratio[i],
                             debt_ratio=debt_ratio[i],
                             income_tax_portion_of_operating_profit=income_tax_portion_of_operating_profit[i],
                             interest_income_to_assets_ratio=interest_income_to_assets_ratio[i],
                             interest_income_margin=interest_income_margin[i],
                             return_on_investment=return_on_investment[i],
                             commission_to_operating_income=commission_to_operating_income[i],
                             net_profit_margin=net_profit_margin[i],
                             staff_expense_to_income_ratio=staff_expense_to_income_ratio[i],
                             loan_to_deposit_ratio=loan_to_deposit_ratio[i],
                             )
        risk=[round(num) for num in risk]
        risk_array.append(risk)
        i=i+1

    return risk_array


#print(risk_analysis(datafile='D:/python tesseract/z score/3d_zscore_table.csv',bank='Civil Bank',quarter='Q2 2072'))

# Example usage
#x=risk_analysis_from_input(datafile='D:/python tesseract/z outp/z output/z_scores.csv', quarter='Q2 2068')



