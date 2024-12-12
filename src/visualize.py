import pandas as pd
import matplotlib.pyplot as plt

def generate_report(data):
    return data.groupby(['Category', 'Subcategory'])['Amount'].sum().reset_index()

def create_summary_chart(data):
    summary = data.groupby('Category')['Amount'].sum().reset_index()

    # Define basic colors for categories
    colors = {'Income': 'green', 'Expense': 'red'}

    # Create a simple bar chart
    plt.bar(summary['Category'], summary['Amount'], color=summary['Category'].map(colors))

    # Set title and labels
    plt.title('Income vs Expense', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Amount', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Save the chart as a PNG file
    plt.savefig('data/summary_chart.png', format='png', dpi=300)
    plt.close()

def create_summary_pie(data):
    # Group data by Category and sum the amounts
    summary = data.groupby('Category')['Amount'].sum().reset_index()

    # Initialize variables for income and expenses
    income = 0
    expense = 0

    # Iterate over the summary and accumulate totals for income and expenses
    for _, row in summary.iterrows():
        if row['Category'] == 'Income':
            income += row['Amount']
        elif row['Category'] == 'Expense':
            expense += abs(row['Amount'])  # Ensure expenses are positive

    # Prepare labels, sizes, and colors for the pie chart
    labels = ['Income', 'Expense']
    sizes = [income, expense]
    colors = ['yellow', 'blue']

    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'black'}
    )

    plt.title('Income vs Expense', fontsize=16)
    plt.savefig('data/summary_pie.png', format='png', dpi=300)
    plt.close()


def create_combined_chart(data):
    # Create subplots: 3 rows and 1 column (vertically stacked)
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # 1. Category-wise Expenses (Bar Chart)
    category_expenses = data[data['Category'] == 'Expense'].groupby('Subcategory')['Amount'].sum().reset_index()
    axs[0].bar(category_expenses['Subcategory'], category_expenses['Amount'], color='red')
    axs[0].set_title('Category-wise Expenses', fontsize=14)
    axs[0].set_xlabel('Subcategory', fontsize=12)
    axs[0].set_ylabel('Total Expense', fontsize=12)
    axs[0].tick_params(axis='x', rotation=45)

    # 2. Monthly Trends (Stacked Bar Chart)
    data['Month'] = pd.to_datetime(data['Date']).dt.to_period('M')
    monthly_summary = data.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)
    monthly_summary.plot(kind='bar', stacked=True, ax=axs[1], color=['green', 'red'])
    axs[1].set_title('Monthly Income and Expense Trends', fontsize=14)
    axs[1].set_xlabel('Month', fontsize=12)
    axs[1].set_ylabel('Total Amount', fontsize=12)
    axs[1].tick_params(axis='x', rotation=45)

    # 3. Income-Expense Ratio (Bar Chart)
    total_income = data[data['Category'] == 'Income']['Amount'].sum()
    total_expense = data[data['Category'] == 'Expense']['Amount'].sum()
    ratio = total_income / abs(total_expense) if total_expense != 0 else 0
    categories = ['Income', 'Expense']
    values = [total_income, abs(total_expense)]
    colors = ['green', 'red']
    axs[2].bar(categories, values, color=colors)
    axs[2].set_title(f'Income-Expense Ratio: {ratio:.2f}', fontsize=14)
    axs[2].set_xlabel('Category', fontsize=12)
    axs[2].set_ylabel('Amount', fontsize=12)

    # Adjust layout to avoid overlap
    plt.tight_layout()

    # Save the combined chart as a PNG file
    plt.savefig('data/combined_analysis.png', format='png', dpi=300)