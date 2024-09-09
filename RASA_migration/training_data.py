import pandas as pd
import random

# Sample DataFrame
data = {
    "Trade Date": ["03/05/2020", "12/01/2021", "06/15/2022"],
    "Transaction Amount": ["$1,500.50", "$3,250.75", "$5,100.00"],
    "Status": ["Completed", "Pending", "Failed"],
    "Trade ID": ["12345", "67890", "54321"],
    "Counterparty Name": ["John Doe", "Jane Smith", "Michael Johnson"]
}
df = pd.DataFrame(data)

# List of query templates with placeholders for dynamic value injection
query_templates = [
    "The trade was executed on {Trade Date} for an amount of {Transaction Amount}.",
    "Status of the transaction with Trade ID {Trade ID} is {Status}.",
    "The trade with Trade ID {Trade ID} with {Counterparty Name} was {Status}.",
    "The transaction dated {Trade Date} with amount {Transaction Amount} has been {Status}.",
    "Counterparty {Counterparty Name} has initiated a trade with Trade ID {Trade ID} on {Trade Date}."
]

# Function to generate dynamic training samples
def generate_training_data_from_df(df, num_samples=10):
    training_data = []
    
    for i in range(num_samples):
        # Randomly pick a query template
        query_template = random.choice(query_templates)
        
        # Replace placeholders with random values from the DataFrame
        query = query_template
        entity_dict = {}
        for column in df.columns:
            if f"{{{column}}}" in query_template:
                value = random.choice(df[column].tolist())
                query = query.replace(f"{{{column}}}", f"[{value}]({column})")  # Annotate the entity
                entity_dict[column] = value
        
        # Append the annotated query to the training data
        training_data.append(query)
    
    return training_data

# Function to generate NLU YAML format
def generate_nlu_yaml_format(training_data):
    yaml_data = "- intent: inform\n  examples: |\n"
    
    for query in training_data:
        yaml_data += f"    - {query}\n"
    
    return yaml_data

# Generate training data from the DataFrame
training_data = generate_training_data_from_df(df, num_samples=10)

# Generate NLU YAML formatted data
nlu_yaml_format = generate_nlu_yaml_format(training_data)

# Output the NLU YAML data to a file
with open("nlu.yml", "w") as file:
    file.write(nlu_yaml_format)

print("Training data in nlu.yml format has been generated and saved to nlu.yml.")
