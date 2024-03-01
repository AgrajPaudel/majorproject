import pandas as pd
import numpy as np
from final_project_4d_z_score import get_values_for_variable_bank_quarter
from sklearn.neighbors import NearestNeighbors
import joblib


def calculate_rms_distance(array1, array2):
    valid_mask = ~np.isnan(array1) & ~np.isnan(array2)
    valid_indices = np.where(valid_mask)[0]
    if len(valid_indices) > 0:
        squared_diff = np.square(array1[valid_indices] - array2[valid_indices])
        mean_squared_diff = np.mean(squared_diff)
        rms_distance = np.sqrt(mean_squared_diff)
        return rms_distance
    else:
        return np.nan


def get_column_data(datafile):
    result_dict = {}
    df_file = pd.read_csv(datafile, index_col=[0, 'Bank'])
    banks = df_file.index.get_level_values(1).unique()
    quarters = df_file.columns
    required_variables = [
        "capital fund to rwa",
        "non performing loan to total loan",
        "total loan loss provision to npl",
        "cost of fund",
        "base rate",
        "net interest spread",
        "return on equity",
        "return on total assets",
        "credit to deposit ratio",
        "debt ratio",
        "return on investment",
        "net profit margin",
    ]

    all_values = []
    all_indices = []

    for bank in banks:
        for quarter in quarters:
            value_of_variables = []
            for variable in required_variables:
                value_of_variables.append(get_values_for_variable_bank_quarter(datafile=datafile,
                                                                               variable=variable,
                                                                               quarter=quarter,
                                                                               bank=bank))

            all_values.append(value_of_variables)
            all_indices.append((bank, quarter))

    all_values = np.array(all_values)

    return all_values, all_indices


def build_knn_model(datafile):
    all_values, all_indices = get_column_data(datafile)

    # Calculate pairwise RMS distances
    rms_distances = []
    for i in range(len(all_values)):
        rms_dist_row = []
        for j in range(len(all_values)):
            if i != j:
                rms_dist = calculate_rms_distance(all_values[i], all_values[j])
                if not np.isnan(rms_dist):
                    rms_dist_row.append(rms_dist)
                else:
                    rms_dist_row.append((1000))
            else:
                rms_dist_row.append(1000)
        rms_distances.append(rms_dist_row)

    rms_distances = np.array(rms_distances)

    knn_model = NearestNeighbors(n_neighbors=5, metric='precomputed').fit(rms_distances)

    # Save the model and data
    joblib.dump((knn_model, all_values, all_indices), 'knn_model_data.pkl')


def load_knn_model(filename):
    return joblib.load(filename)


def get_nearest_datasets(model, input_array, all_values, all_indices):
    rms_distances = []
    for i in range(len(all_values)):
        rms_dist = calculate_rms_distance(input_array, all_values[i])
        if not np.isnan(rms_dist):
            rms_distances.append(rms_dist)
        else:
            rms_distances.append((1000))

    rms_distances = np.array(rms_distances)

    distances, indices = model.kneighbors(rms_distances.reshape(1, -1))

    nearest_datasets = [(all_indices[i], distances[0][j]) for j, i in enumerate(indices[0])]

    return nearest_datasets


# Example usage to build and save the model
#datafile = '3d data/data_cube.csv'
#build_knn_model(datafile)

# Example usage to load the model and data
#knn_model, all_values, all_indices = load_knn_model('knn_model_data.pkl')

# Example usage to get nearest datasets
#input_array = np.random.rand(12)  # Example input array
#nearest_datasets = get_nearest_datasets(knn_model, input_array, all_values, all_indices)
#print(nearest_datasets)
