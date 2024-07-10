import pandas as pd
import re

def word_count(text):
    return len(re.findall(r'\b\w+\b', str(text)))

def char_count(text):
    return len(str(text))

def sentence_count(text):
    return len(re.findall(r'[^.!?]+[.!?]', str(text)))

def average_word_length(text):
    words = re.findall(r'\b\w+\b', str(text))
    return sum(len(word) for word in words) / len(words) if words else 0

def average_sentence_length(text):
    sentences = re.findall(r'[^.!?]+[.!?]', str(text))
    words = re.findall(r'\b\w+\b', str(text))
    return len(words) / len(sentences) if sentences else 0

def length_analysis(column):
    return {
        'word_count': column.apply(word_count).sum(),
        'char_count': column.apply(char_count).sum(),
        'sentence_count': column.apply(sentence_count).sum(),
        'average_word_length': column.apply(average_word_length).mean(),
        'average_sentence_length': column.apply(average_sentence_length).mean()
    }

# Define the input and output Excel file paths
input_file = 'input.xlsx'  # Change this to your input file path
output_file = 'output_analysis.xlsx'  # Change this to your desired output file path

# Read the Excel file
df = pd.read_excel(input_file, sheet_name='MCA')

# Check if the column "QUERY" exists in the DataFrame
if 'QUERY' in df.columns:
    # Perform length analysis on the "QUERY" column
    analysis_result = length_analysis(df['QUERY'])

    # Convert the result to a DataFrame
    analysis_df = pd.DataFrame(analysis_result, index=[0])

    # Write the analysis DataFrame to a new Excel file
    analysis_df.to_excel(output_file, index=False)

    print("Length analysis completed. Check the output Excel file.")
else:
    print("The column 'QUERY' does not exist in the sheet 'MCA'.")
