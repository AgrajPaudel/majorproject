import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.impute import SimpleImputer
from joblib import load
from itertools import combinations
import numpy as np


def visualize_data_from_pickle(file_path):
    # Load data from pickle file
    with open(file_path, 'rb') as f:
        knn_model, all_values, all_indices = load(f)

    # Preprocess data to handle NaN values
    imputer = SimpleImputer(strategy='mean')
    all_values = imputer.fit_transform(all_values)

    # Get number of variables
    num_variables = all_values.shape[1]

    # Get unique classes
    unique_classes = np.unique(all_indices)

    # Create combinations of variables
    variable_combinations = list(combinations(range(num_variables), 2))

    # Create a PDF to save the plots
    pdf_path = 'visualization_plots.pdf'
    with PdfPages(pdf_path) as pdf:
        # Plot the data for each combination of variables
        for idx, (var1, var2) in enumerate(variable_combinations, start=1):
            plt.figure(figsize=(8, 6))
            for class_ in unique_classes:
                class_indices = np.where(all_indices == class_)[0]
                plt.scatter(all_values[class_indices, var1], all_values[class_indices, var2], label=f'Class {class_}', alpha=0.7)
            plt.title(f'Variable {var1 + 1} vs Variable {var2 + 1}')
            plt.xlabel(f'Variable {var1 + 1}')
            plt.ylabel(f'Variable {var2 + 1}')
            plt.grid(True)
            plt.ylim(0,10)
            plt.xlim(10,20)
            plt.legend()
            pdf.savefig()  # Save the plot to the PDF
            plt.close()

    print(f'Plots saved to {pdf_path}')

# Example usage
file_path = 'D:/python tesseract/knn_model_data11.pkl'
visualize_data_from_pickle(file_path)