import pandas as pd
from final_project_4d_z_score import display_all_quarters_and_banks_for_variable
from final_project_4d_z_score import  display_all_banks_for_quarter_and_variable
from final_project_extract_data_from_input import get_values_for_quarter_and_variable
import numpy as np
import os
filepath='D:/python tesseract/3d data/data_cube.csv'

def shave_off_last_file(path):
    # Split the path into its directory and filename components
    directory, filename = os.path.split(path)
    # Remove the last filename from the path
    return directory

class VariableInfo:
    def __init__(self,datafile,quarter, variable_name, first_value, second_value):
        self.variable_name = variable_name
        self.values = [first_value, second_value]
        self.outlier = self.check_outlier()
        ###############################
        total_values = display_all_quarters_and_banks_for_variable(datafile=filepath, variable=variable_name)
        quarter_values = display_all_banks_for_quarter_and_variable(datafile=filepath, variable=variable_name,
                                                                    quarter=quarter)
        self.totals_mean = np.mean(total_values)
        self.quarter_mean = np.mean(quarter_values)
        self.self_value = get_values_for_quarter_and_variable(quarter=quarter,variable=variable_name,datafile=os.path.join(shave_off_last_file(datafile),'merged_file.csv'))

    def check_outlier(self):
        # Check if the first value is an outlier based on Z-score threshold
        if self.values[0] and self.values[0] != 'nan':
            z_score_threshold = 1.645
            return float(self.values[0]) < -z_score_threshold or float(self.values[0]) > z_score_threshold
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
        return f"Variable: {self.variable_name}, Values: {self.values}, Outlier: {self.outlier}"


def extract_z_scores(variable_and_z_scores, variable_name):
    for variable, z_scores in variable_and_z_scores:
        if variable == variable_name:
            return z_scores


def display_quarter_data(datafile, quarter):
    # Read the data cube CSV file
    df = pd.read_csv(datafile, index_col=0)

    try:
        # Use loc to access data for the specified quarter
        result = df.loc[:, quarter]
        variable_names = result.index.tolist()

        # Extract values from the result DataFrame
        values = result.values.flatten().tolist()

        # Create a 2D array
        variable_data = list(zip(variable_names, values))

        return variable_data

    except KeyError:
        print(f"Data not found for quarter: {quarter}")


def get_variable_info(datafile, quarter):
    variable_data = display_quarter_data(datafile=datafile, quarter=quarter)
    variable_objects = [
        VariableInfo(datafile,quarter,variable, *values.split()) if isinstance(values, str) and values != 'nan' else VariableInfo(
            datafile,quarter,variable, 'nan', 'nan')
        for variable, values in variable_data
    ]

    return [variable_object.to_json() for variable_object in variable_objects]

#print(shave_off_last_file('D:/python tesseract/z outp/z output/z_scores.csv'))
#print(get_variable_info(datafile='D:/python tesseract/z outp/z output/z_scores.csv',quarter='Q4 2079'))
