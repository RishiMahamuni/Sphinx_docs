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

def length_analysis(row):
    return {
        'word_count': word_count(row),
        'char_count': char_count(row),
        'sentence_count': sentence_count(row),
        'average_word_length': average_word_length(row),
        'average_sentence_length': average_sentence_length(row)
    }

# Define the input and output Excel file paths
input_file = 'input.xlsx'  # Change this to your input file path
output_file = 'output_analysis.xlsx'  # Change this to your desired output file path

# Read the Excel file
df = pd.read_excel(input_file, sheet_name='MCA')

# Check if the column "QUERY" exists in the DataFrame
if 'QUERY' in df.columns:
    # Perform length analysis on each row in the "QUERY" column
    analysis_results = df['QUERY'].apply(length_analysis)

    # Convert the results to a DataFrame
    analysis_df = pd.DataFrame(list(analysis_results))

    # Combine the original DataFrame with the analysis DataFrame
    result_df = pd.concat([df, analysis_df], axis=1)

    # Write the combined DataFrame to a new Excel file
    result_df.to_excel(output_file, index=False)

    print("Length analysis completed. Check the output Excel file.")
else:
    print("The column 'QUERY' does not exist in the sheet 'MCA'.")
