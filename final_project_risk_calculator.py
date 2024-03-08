import math

def convert_to_numeric(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def risk_calculator(**kwargs):
    # Define camel score categories for good and bad variables
    good_camel_score_categories = {
        1: (0.84, float('inf')),
        2: (0.25, 0.84),
        3: (-0.25, 0.25),
        4: (-0.84, -0.25),
        5: (-float('inf'), -0.84)
    }

    bad_camel_score_categories = {
        1: (-float('inf'), -0.84),
        2: (-0.84, -0.25),
        3: (-0.25, 0.25),
        4: (0.25, 0.84),
        5: (0.84, float('inf'))
    }

    # Define categories for CAMELS
    camel_categories = {
        'c': ['capital_fund_to_rwa'],
        'a': ['return_on_total_assets', 'return_on_equity', 'credit_to_deposit_ratio', 'income_tax_portion_of_operating_profit',
              'interest_income_to_assets_ratio', 'interest_income_margin', 'return_on_investment', 'net_profit_margin'],
        'm': ['cost_of_fund'],
        'e': ['net_interest_spread', 'return_on_investment', 'net_profit_margin',
              'income_tax_portion_of_operating_profit', 'staff_expense_to_income_ratio'],
        'l': ['credit_to_deposit_ratio', 'loan_to_deposit_ratio'],
        's': ['base_rate', 'interest_income_to_assets_ratio', 'interest_income_margin'],
    }

    camel_scores = {category: [] for category in camel_categories}

    for key, val in kwargs.items():
        if key in camel_categories['c']:
            score_category = 'c'
        elif key in camel_categories['a']:
            score_category = 'a'
        elif key in camel_categories['m']:
            score_category = 'm'
        elif key in camel_categories['e']:
            score_category = 'e'
        elif key in camel_categories['l']:
            score_category = 'l'
        elif key in camel_categories['s']:
            score_category = 's'
        else:
            continue  # Skip if key does not belong to any category

        numeric_val = convert_to_numeric(val)
        if numeric_val is not None:
            # Calculate camel score for the variable
            if key == 'credit_to_deposit_ratio':
                if -0.85 <= numeric_val < -0.25 or 0.25 < numeric_val <= 0.85:
                    camel_scores[score_category].append(3)
                elif numeric_val < -0.85 or numeric_val > 0.85:
                    camel_scores[score_category].append(5)
                else:
                    camel_scores[score_category].append(1)
            else:
                # Determine which camel score category to use based on good or bad variable
                camel_score_categories = good_camel_score_categories if key not in ['debt_ratio', 'cost_of_fund',
                                                                                     'non_performing_loan_to_total_loan',
                                                                                     'commission_to_operating_income',
                                                                                     'base_rate', 'staff_expense_to_income_ratio',
                                                                                     'loan_to_deposit_ratio',
                                                                                     'income_tax_portion_of_operating_profit'] else bad_camel_score_categories

                # Calculate camel score for the variable
                for score, (lower_bound, upper_bound) in camel_score_categories.items():
                    if lower_bound < numeric_val <= upper_bound:
                        camel_scores[score_category].append(score)
                        break  # Once we've found the score, move to the next variable
                else:
                    print(f"Value for {key} is out of range")
        else:
            print(f"Unable to convert value for {key} to numeric")

    # Calculate CAMELS scores
    camel_results = []
    for category, scores in camel_scores.items():
        if scores:
            mean_score = sum(scores) / len(scores)
            camel_results.append(mean_score)
        else:
            camel_results.append(float('nan'))  # If no scores available, set to NaN

    return camel_results



