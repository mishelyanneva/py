import os
import pandas as pd
from src.preprocess import normalize_description
from src.classify import classify_transaction
from src.visualize import generate_report, create_summary_chart, create_summary_pie, create_combined_chart


# Define file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(base_dir, "data", "transactions.csv")
output_file = os.path.join(base_dir, "data", "report.csv")

# Load data
data = pd.read_csv(input_file)

# Preprocess descriptions
print("Normalizing transaction descriptions...")
data['Normalized_Description'] = data['Description'].apply(normalize_description)

# Classify transactions
print("Classifying transactions into categories and subcategories...")
data[['Category', 'Subcategory']] = data.apply(
    lambda row: classify_transaction(row['Normalized_Description'], row['Amount']),
    axis=1, result_type='expand'
)

# Generate a report
print("Generating transaction report...")
report = generate_report(data)
report.to_csv(output_file, index=False)

# Create a summary chart
print("Creating summary chart visualization...")
create_summary_chart(data)

# Create a pie chart
print("Creating summary pie chart visualization...")
create_summary_pie(data)
# Generate the report
print("Generating transaction report...")
report = generate_report(data)
report.to_csv(output_file, index=False)

# Create visualizations
print("Creating summary chart visualization...")
create_summary_chart(data)

print("Creating summary pie chart visualization...")
create_summary_pie(data)

# Generate the report
print("Generating transaction report...")
report = generate_report(data)
report.to_csv(output_file, index=False)

# Create the combined chart with multiple analyses
print("Creating combined analysis chart...")
create_combined_chart(data)

print(f"Workflow completed successfully! \n- Report saved to: {output_file}\n- Combined analysis saved to: data/combined_analysis.png")
