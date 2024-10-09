import pandas as pd

# Load the existing CSV with wrap-up codes
existing_wrapups = pd.read_csv('wrapup_codes.csv')

# Load the new CSV with wrap-up codes to add
new_wrapups = pd.read_csv('input.csv')

# Concatenate the two DataFrames, ignoring any duplicate codes
combined_wrapups = pd.concat([existing_wrapups, new_wrapups]).drop_duplicates(subset=['name'], keep='first')

# Save the updated CSV
combined_wrapups.to_csv('wrapup_codes.csv', index=False)

print("Wrap-up codes added successfully!")
