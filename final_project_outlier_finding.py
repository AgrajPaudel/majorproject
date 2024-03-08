import numpy as np
import pandas as pd
from final_project_4d_z_score import display_all_quarters_and_banks_for_variable
from final_project_4d_z_score import  display_all_banks_for_quarter_and_variable
from final_project_1_extract_unit_data import display_value_for_variable_bank_quarter
import json

filepath='D:/python tesseract/3d data/data_cube.csv'
def extract_z_scores(variable_and_z_scores, variable_name):
    for variable, z_scores in variable_and_z_scores:
        if variable == variable_name:
            return z_scores


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


class VariableInfo:
    def __init__(self,bank,datafile,quarter, variable_name, first_value, second_value, third_value):
        self.variable_name = variable_name
        self.values = [first_value, second_value, third_value]
        self.outlier = self.check_outlier()
        #################
        total_values = display_all_quarters_and_banks_for_variable(datafile=filepath, variable=variable_name)
        quarter_values = display_all_banks_for_quarter_and_variable(datafile=filepath, variable=variable_name,
                                                                    quarter=quarter)
        self.totals_mean = np.mean(total_values)
        self.quarter_mean = np.mean(quarter_values)
        self.self_value = display_value_for_variable_bank_quarter(variable=variable_name,bank=bank,quarter=quarter,datafile=filepath)

    def check_outlier(self):
        # Check if the first value is an outlier based on Z-score threshold
        if self.values[1] and self.values[1] != 'nan':
            z_score_threshold = 1.645
            return float(self.values[1]) < -z_score_threshold or float(self.values[1]) > z_score_threshold
        return False




    def to_json(self):
        return {
            "variable": self.variable_name,
            "values": self.values,
            "outlier": self.outlier,
            "totals_mean": str(self.totals_mean),
            "quarter_mean": str(self.quarter_mean),
            "self_value": str(self.self_value),
        }

    def __str__(self):
        return f"Variable: {self.variable_name}, Values: {self.values}, Outlier: {self.outlier}, Totals Mean: {self.totals_mean}, Quarter Mean: {self.quarter_mean}, Self Value: {self.self_value}"


def get_variable_info(datafile, quarter, bank):
    variable_data = display_bank_quarter_data(datafile=datafile, quarter=quarter, bank=bank)

    variable_objects = [
        VariableInfo(bank,datafile,quarter,variable, *values.split()) if isinstance(values, str) and values != 'nan' else VariableInfo(bank,datafile,quarter,variable, 'nan', 'nan', 'nan')
        for variable, values in variable_data
    ]


    return [variable_object.to_json() for variable_object in variable_objects]


