import os

from src.preprocess import (
    preprocess_text,
    feature_extraction,
    FlexibleTableProcessor
)
from src.classify import classify_transaction
from src.visualize import (
    generate_report,
    create_summary_chart,
    create_summary_barchart,
    create_combined_chart,
)

def main():
    # Define file paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data", "transactions.csv")
    output_file = os.path.join(base_dir, "data", "report.csv")

    # Initialize Flexible Table Processor
    table_processor = FlexibleTableProcessor(
        required_columns=['Description', 'Amount', 'Date'],
        date_columns=['Date'],
        numeric_columns=['Amount']
    )

    # Load and preprocess data
    print("Loading and preprocessing data...")
    try:
        # Use flexible table loader
        data = table_processor.load_flexible_table(input_file)

        # Validate table structure
        structure_analysis = table_processor.validate_table_structure(data)
        print("Table Structure Analysis:")
        print(f"Total Columns: {structure_analysis['total_columns']}")
        print(f"Columns: {structure_analysis['columns']}")
        print(f"Missing Required Columns: {structure_analysis['missing_required_columns']}")

        # Preprocess descriptions
        print("Normalizing transaction descriptions...")
        data['Normalized_Description'] = data['Description'].apply(preprocess_text)

        # Extract features using TF-IDF
        print("Extracting text features...")
        features, feature_names = feature_extraction(data['Normalized_Description'])
        data['TF-IDF_Features'] = list(features.toarray())

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

        # Create visualizations
        print("Creating summary chart visualizations...")
        create_summary_chart(data)  # General summary chart
        create_summary_barchart(data)    # Monthly pie charts (new functionality)
        create_combined_chart(data)

        print(f"Workflow completed successfully! \n"
              f"- Report saved to: {output_file}\n"
              f"- Combined analysis saved to: "
              f"data/combined_analysis.png, "
              f"data/summary_chart.png, "
              f"data/summary_barchart.png")

    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
