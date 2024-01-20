import pandas as pd


class VariableInfo:
    def __init__(self, variable_name, first_value, second_value):
        self.variable_name = variable_name
        self.values = [first_value, second_value]
        self.outlier = self.check_outlier()

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
            "outlier": self.outlier
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
        VariableInfo(variable, *values.split()) if isinstance(values, str) and values != 'nan' else VariableInfo(
            variable, 'nan', 'nan')
        for variable, values in variable_data
    ]

    return [variable_object.to_json() for variable_object in variable_objects]



