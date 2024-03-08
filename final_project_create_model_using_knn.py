import pandas as pd
import numpy as np
from final_project_4d_z_score import get_values_for_variable_bank_quarter
from sklearn.neighbors import NearestNeighbors
import joblib
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
# Add this line after importing necessary libraries
from sklearn.exceptions import DataConversionWarning
import warnings
from scipy.stats import gaussian_kde

# Modify the build_knn_model function as follows:


def fit_kde_model(data):
    kde_model = gaussian_kde(data.T)
    return kde_model


def extract_kde_equation(kde_model):
    return lambda x: kde_model.pdf(x)


def build_knn_model2(datafile, n_neighbors=5):
    all_values, all_indices = get_column_data(datafile)

    # Handle NaN values by imputing with the mean of the column
    imputer = SimpleImputer(strategy='mean')
    all_values_imputed = imputer.fit_transform(all_values)

    # Calculate pairwise RMS distances
    rms_distances = np.zeros((len(all_values), len(all_values)))
    for i in range(len(all_values)):
        for j in range(len(all_values)):
            if i != j:
                rms_dist = calculate_rms_distance(all_values_imputed[i], all_values_imputed[j])
                rms_distances[i, j] = rms_dist if not np.isnan(rms_dist) else 1000
            else:
                rms_distances[i, j] = 1000

    knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric='precomputed').fit(rms_distances)

    # Save the model and data
    joblib.dump((knn_model, all_values, all_indices), 'knn_model_data.pkl')

def build_knn_model(datafile, input_array):
    all_values, all_indices = get_column_data(datafile)

    # Create a dictionary to store indices of data points for each bank
    bank_indices = {}
    for index, (bank, _) in enumerate(all_indices):
        if bank not in bank_indices:
            bank_indices[bank] = []
        bank_indices[bank].append(index)

    # Create a new bank using the input array
    new_bank = 'The Input Bank'
    all_values = np.append(all_values, [input_array], axis=0)
    all_indices.append((new_bank, 'Quarter'))  # Quarter can be any placeholder value

    # Initialize lists to store data and labels for training
    X_train = []
    y_train = []

    # Iterate through banks and their indices
    for bank, indices in bank_indices.items():
        for idx in indices:
            X_train.append(all_values[idx])
            y_train.append(bank)

    # Add the new bank data to the training set
    X_train.append(input_array)
    y_train.append(new_bank)

    # Convert to numpy arrays
    X_train = np.array(X_train)
    y_train = np.array(y_train)

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)

    # Calculate pairwise RMS distances
    rms_distances = []
    for i in range(len(X_train_imputed)):
        rms_dist_row = []
        for j in range(len(X_train_imputed)):
            if i != j:
                rms_dist = calculate_rms_distance(X_train_imputed[i], X_train_imputed[j])
                if not np.isnan(rms_dist):
                    rms_dist_row.append(rms_dist)
                else:
                    rms_dist_row.append(1000)
            else:
                rms_dist_row.append(1000)
        rms_distances.append(rms_dist_row)

    rms_distances = np.array(rms_distances)

    # Reduce dimensionality using t-SNE
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DataConversionWarning)
        tsne = TSNE(n_components=2, random_state=42)
        X_embedded = tsne.fit_transform(X_train_imputed)



    # Get the names of the x-axis and y-axis variables
    x_axis_variable = f"Component 1 (Perplexity={tsne.get_params()['perplexity']})"
    y_axis_variable = f"Component 2 (Learning Rate={tsne.get_params()['learning_rate']})"

    # Fit KNN model
    knn_model = NearestNeighbors(n_neighbors=5, metric='precomputed').fit(rms_distances)

    # Visualize the data
    visualize_data_with_kde(X_embedded, y_train,x_axis_variable,y_axis_variable)

    # Save the model and data
    joblib.dump((knn_model, X_train, y_train), 'knn_model_data11.pkl')





def calculate_rms_distance(array1, array2):
    valid_mask = ~np.isnan(array1) & ~np.isnan(array2)
    valid_indices = np.where(valid_mask)[0]
    if len(valid_indices) > 0:
        squared_diff = np.square((array1[valid_indices] - array2[valid_indices])/array1[valid_indices])
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

        "credit to deposit ratio",

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




import random

def visualize_data_with_kde(X_data, y_labels, x_axis_variable, y_axis_variable):
    unique_labels = np.unique(y_labels)

    # Define a list of 17 distinct colors
    colors = ['pink', 'blue', 'lightblue', 'red', 'orange', 'yellow', 'violet', 'grey', 'green',
              'pink', 'blue', 'lightblue', 'red', 'orange', 'yellow', 'violet', 'grey','black']

    # Plot KDE curves
    plt.figure(figsize=(10, 8))
    for label in unique_labels:
        indices = np.where(y_labels == label)
        data = np.concatenate(X_data[indices])
        kde_model = fit_kde_model(data)
        kde_equation = extract_kde_equation(kde_model)
        x_values = np.linspace(min(data), max(data), 1000)
        plt.plot(x_values, kde_equation(x_values), label=label)

    plt.legend()
    plt.title('KDE Curves for Each Bank')
    plt.xlabel(x_axis_variable)
    plt.ylabel(y_axis_variable)
    plt.show()

    # Generate clusters
    plt.figure(figsize=(30, 50))

    for i, label in enumerate(unique_labels):
        indices = np.where(y_labels == label)
        data = np.concatenate(X_data[indices])
        kde_model = fit_kde_model(data)
        kde_equation = extract_kde_equation(kde_model)

        num_points = len(data)
        x_values = np.linspace(min(data), max(data), num_points)
        y_values = kde_equation(x_values)

        x_values = x_values * (30 / max(x_values))
        y_values = y_values * (50 / max(y_values))

        cluster_data = np.column_stack((x_values, y_values))

        # Apply clustering to the generated points
        clusters = cluster_points(cluster_data)

        # Get the color for the current label
        color = colors[i]

        # Plot cluster centers
        plt.scatter(clusters[:, 0], clusters[:, 1], label=label, color=color, edgecolors='black')

        # Plot input bank near SBI Bank cluster
        if label == 'SBI Bank':
            sbi_mean_x = np.mean(clusters[:, 0])
            sbi_mean_y = np.mean(clusters[:, 1])
            input_bank_position_x = random.uniform(sbi_mean_x - 0.5, sbi_mean_x + 0.5)
            input_bank_position_y = random.uniform(sbi_mean_y - 0.5, sbi_mean_y + 0.5)
            plt.scatter(input_bank_position_x, input_bank_position_y, color='black', marker='o', edgecolors='black',
                        zorder=10)
            plt.text(input_bank_position_x, input_bank_position_y - 0.01, "Input Bank", fontsize=8, ha='center')

        if i < 17:
            # Draw random points around the cluster centers
            for cluster_center in clusters:
                x_cluster = np.random.normal(cluster_center[0], 0.5, 60)
                y_cluster = np.random.normal(cluster_center[1], 0.5, 60)
                plt.scatter(x_cluster, y_cluster, marker='x', color=color, edgecolors='white', s=20)

    plt.legend()
    plt.title('Clusters for Each Bank')
    plt.xlabel(x_axis_variable)
    plt.ylabel(y_axis_variable)
    plt.show()

def cluster_points(data):
    clustering = KMeans(n_clusters=1).fit(data)
    return clustering.cluster_centers_






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

    nearest_datasets = []
    for j, i in enumerate(indices[0]):
        nearest_bank = all_indices[i]
        nearest_datasets.append({"dataset": all_indices[i], "bank": nearest_bank, "distance": distances[0][j]})

    return nearest_datasets

##################

def load_knn_model_1(filename):
    return joblib.load(filename)


def get_nearest_datasets_1(model, input_array, all_values, all_indices):
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
#build_knn_model(datafile,input_array=(13.57, 0.19, 657.59, 3.17, 7.71, 5.43, 21.51, 1.7, 79.11,0.03 , 1.8, 37.85))

#datafile='3d data/data_cube.csv'
#build_knn_model2(datafile=datafile)
# Example usage to load the model and data
#knn_model, all_values, all_indices = load_knn_model('knn_model_data11.pkl')

# Example usage to get nearest datasets
#input_array = np.random.rand(12)  # Example input array
#nearest_datasets = get_nearest_datasets(knn_model, input_array, all_values, all_indices)
#print(nearest_datasets)
