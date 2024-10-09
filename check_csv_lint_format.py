import pandas as pd
import csv
import os


def validate_csv(file_path, required_columns=None, column_types=None, expected_column_count=None):
    """Validate a CSV file for various conditions."""
    
    # 1. Check if file exists
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    try:
        # 2. Try loading the CSV into a pandas DataFrame
        df = pd.read_csv(file_path)

        # 3. Check if required columns are present (optional)
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return f"Error: Missing required columns: {missing_columns}"

        # 4. Check if the number of columns is consistent
        if df.isnull().any().any():
            return "Error: CSV contains missing values."

        # 5. Check if any row has more columns than expected
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            # Initialize a flag to indicate if any row exceeds the column limit
            exceeds_limit = False
            
            # Iterate over each row in the CSV
            for row_number, row in enumerate(csv_reader, start=1):
                # Check the number of columns in the current row
                if len(row) > expected_column_count:
                    exceeds_limit = True
                    print(f"Row {row_number} has {len(row)} columns: {row}. Number of required columns are {expected_column_count}.")         

        # 6. Check if each column has the correct data type
        if column_types:
            for column, expected_type in column_types.items():
                if column in df.columns:
                    if not df[column].map(type).eq(expected_type).all():
                        return f"Error: Column '{column}' does not contain all {expected_type.__name__} types."

        # 6. Check for duplicates
        if df.duplicated().any():
            return "Error: CSV contains duplicate rows."

        # If everything is fine
        return "CSV is valid."

    except pd.errors.EmptyDataError:
        return "Error: CSV is empty."
    except pd.errors.ParserError:
        return "Error: CSV is malformed or has inconsistent column counts."
    except Exception as e:
        return f"Error: {e}"


file_path = "input.csv"
required_columns = ["Name", "Age", "Email"]  #  expected columns names
column_types = {"Age": int, "Email": str}    #  expected column types
expected_column_count = len(required_columns)

result = validate_csv(file_path, required_columns, column_types,expected_column_count)
print(result)



