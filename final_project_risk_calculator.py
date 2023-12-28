import math

def convert_to_numeric(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def risk_calculator(**kwargs):
    multipliers = {
        "capital_fund_to_rwa": 1.5,
        "non_performing_loan_to_total_loan": -1.5,
        "total_loan_loss_provision_to_npl": -1,
        "cost_of_fund": -1,
        "base_rate": lambda x: -1 if x < -2 else (-1 if x > 2 else 1),
        "net_interest_spread": 0.5,
        "return_on_equity": 0.5,
        "return_on_total_assets": 0.5,
        "credit_to_deposit_ratio": lambda x: 2 if -2 < x < 2 else -1,
        "debt_ratio": -2,
        "interest_income_to_assets_ratio": 1,
        "interest_income_margin": 1.5,
        "return_on_investment": 2,
        "commission_to_operating_income": -0.5,
        "net_profit_margin": 2,
        "income_tax_portion_of_operating_profit": -1,
        "loan_to_deposit_ratio": -1,
        "staff_expense_to_income_ratio": -1
    }

    numeric_values = {key: convert_to_numeric(val) for key, val in kwargs.items()}

    # Remove None and NaN values
    non_none_values = {key: val for key, val in numeric_values.items() if val is not None and not math.isnan(val)}

    if non_none_values:
        normalization_factor = sum(map(abs, non_none_values.values())) / len(non_none_values)
        normalized_result = {key: val / normalization_factor for key, val in numeric_values.items() if key in non_none_values}
        mean_result = sum(normalized_result.values()) / len(normalized_result)
        return mean_result
    else:
        print('bloo')
        return None
