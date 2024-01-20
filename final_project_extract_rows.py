import pandas as pd
import json

def get_csv_row_headers(file_path):
    try:
        # Read the CSV file with the first column as the index
        df = pd.read_csv(file_path, index_col=0)

        # Get the row headers (index)
        row_headers = df.index.tolist()

        # Convert to JSON format
        result_json = {"variables": row_headers}

        # Print and return the JSON result
        return result_json


    except FileNotFoundError:
        error_msg = {"error": "File not found"}
        print(json.dumps(error_msg, indent=2))
        return error_msg

    except pd.errors.EmptyDataError:
        error_msg = {"error": "Empty CSV file"}
        print(json.dumps(error_msg, indent=2))
        return error_msg

    except Exception as e:
        error_msg = {"error": str(e)}
        print(json.dumps(error_msg, indent=2))
        return error_msg


