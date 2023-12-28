import numpy as np


def calculate_z_score(array, value):
    """
    Calculate the z-score for a given value in an array.

    Parameters:
    - array (numpy array): The array of values.
    - value (float): The value for which the z-score is calculated.

    Returns:
    - float: The z-score of the given value.
    """
    mean = np.mean(array)
    std_dev = np.std(array)

    if std_dev == 0:
        # Handle the case where standard deviation is zero to avoid division by zero
        return np.nan

    z_score = (value - mean) / std_dev
    return z_score