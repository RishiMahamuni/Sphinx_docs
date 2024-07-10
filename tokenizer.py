import pandas as pd

# Define the input and output Excel file paths
input_file = 'input.xlsx'  # Change this to your input file path
output_file = 'output.xlsx'  # Change this to your desired output file path

# Read the Excel file
df = pd.read_excel(input_file, sheet_name='MCA')

# Define the column to be tokenized
column_to_tokenize = 'TextColumn'  # Change this to your column name

# Tokenize the text in the specified column
df['TokenizedText'] = df[column_to_tokenize].apply(lambda x: f"[{', '.join(x.split())}]" if pd.notnull(x) else x)

# Write the modified DataFrame to a new Excel file
df.to_excel(output_file, index=False)

print("Tokenization completed. Check the output Excel file.")
