def interpolate_nan(data):
    interpolated_data = data.copy()  # Create a copy of the input data

    # Iterate over the list, skipping the first and last elements
    for i in range(1, len(data) - 1):
        print(data[i]['value'])
        if data[i]['value'] == 'nan' and data[i-1]['value']!= 'nan' and data[i+1]['value'] != 'nan':
            # If the current element's value is 'nan' and both its neighbors are numbersi1
            interpolated_value = (float(data[i - 1]['value']) + float(data[i + 1]['value'])) / 2  # Interpolate value
            interpolated_data[i]['value'] = interpolated_value  # Update value in the copied data
            interpolated_data[i]['interpolated'] = True  # Mark as interpolated
        else:
            interpolated_data[i]['interpolated'] = False  # Mark as not interpolated

    return interpolated_data