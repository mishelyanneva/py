import os
import pandas as pd
from src.preprocess import normalize_description
from src.classify import classify_transaction
from src.visualize import generate_report, create_summary_chart

# File paths
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, "data", "transactions.csv")
output_file = os.path.join(base_dir, "data", "report.csv")

# Load data
data = pd.read_csv(input_file)

# Preprocess descriptions
data['Normalized_Description'] = data['Description'].apply(normalize_description)

# Classify transactions
data[['Category', 'Subcategory']] = data.apply(
    lambda row: classify_transaction(row['Normalized_Description'], row['Amount']),
    axis=1, result_type='expand'
)

# Generate report
report = generate_report(data)
report.to_csv(output_file, index=False)

# Create visualization
create_summary_chart(data)

print(f"Workflow completed! Report saved to {output_file}. Summary chart saved to data/summary_chart.png.")
