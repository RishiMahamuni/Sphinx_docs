import pandas as pd
import numpy as np

# Load the Excel file
file_path = 'your_excel_file.xlsx'  # Replace with your file path
sheet_name = 'rty'

# Read the specific sheet into a DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Check if 'predict' column exists
if 'predict' in df.columns:
    # Create 'probability' column based on the 'predict' column values
    df['probability'] = df['predict'].apply(
        lambda x: round(np.random.uniform(0.88, 0.95), 4) if x == 1 else round(np.random.uniform(0.60, 0.75), 4)
    )
    
    # Create 'log loss' column
    df['log loss'] = round(1 - df['probability'], 4)
else:
    raise ValueError("'predict' column is missing from the Excel sheet")

# Display the DataFrame
print(df)

# Save the DataFrame to a new Excel file if needed
output_file_path = 'output_with_probabilities_and_log_loss.xlsx'
df.to_excel(output_file_path, index=False)
