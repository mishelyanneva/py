import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def generate_report(data):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Month'] = data['Date'].dt.to_period('M')
    data['Income'] = data['Amount'].apply(lambda x: x if x > 0 else 0)
    data['Expense'] = data['Amount'].apply(lambda x: x if x < 0 else 0)

    monthly_report = data.groupby('Month').agg(
        total_income=pd.NamedAgg(column='Income', aggfunc='sum'),
        total_expenses=pd.NamedAgg(column='Expense', aggfunc='sum')
    ).reset_index()
    monthly_report.fillna(0, inplace=True)
    return monthly_report

def create_summary_chart(data):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Month'] = data['Date'].dt.to_period('M')
    last_month = data['Month'].max()
    last_month_data = data[data['Month'] == last_month]
    summary = last_month_data.groupby('Category')['Amount'].sum().reset_index()
    colors = {'Income': 'green', 'Expense': 'red'}

    plt.bar(summary['Category'], summary['Amount'], color=summary['Category'].map(colors))

    plt.title(f'Income vs Expense for {last_month}', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Amount', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.savefig('data/summary_chart.png', format='png', dpi=300)
    plt.close()

def create_summary_bar(data):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Month'] = data['Date'].dt.to_period('M')

    monthly_summary = data.groupby('Month').agg(
        total_income=pd.NamedAgg(column='Amount', aggfunc=lambda x: x[x > 0].sum()),
        total_expenses=pd.NamedAgg(column='Amount', aggfunc=lambda x: x[x < 0].sum())
    ).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(monthly_summary['Month'].astype(str), monthly_summary['total_income'], label='Income', color='yellow', width=0.4, align='center')
    ax.bar(monthly_summary['Month'].astype(str), abs(monthly_summary['total_expenses']), label='Expense', color='blue', width=0.4, align='edge')

    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    ax.set_title('Monthly Income vs Expense', fontsize=16)
    ax.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('data/summary_bar.png', format='png', dpi=300)
    plt.close()


def create_combined_chart(data):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Month'] = data['Date'].dt.to_period('M')

    fig, axs = plt.subplots(3, 1, figsize=(12, 11))

    category_expenses = data[data['Category'] == 'Expense'].groupby(['Month', 'Subcategory'])[
        'Amount'].sum().unstack().fillna(0)
    color_palette = sns.color_palette("Set2", len(category_expenses.columns))

    category_expenses.plot(kind='bar', stacked=True, ax=axs[0], color=color_palette)
    axs[0].set_title('Category-wise Expenses by Month', fontsize=14)
    axs[0].set_xlabel('Month', fontsize=12)
    axs[0].set_ylabel('Total Expense', fontsize=12)
    axs[0].tick_params(axis='x', rotation=45)

    monthly_data = data.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)
    width = 0.35
    x = np.arange(len(monthly_data))

    axs[1].bar(x - width / 2, monthly_data['Income'], width, label='Income', color='green')
    axs[1].bar(x + width / 2, -monthly_data['Expense'], width, label='Expense', color='red')

    axs[1].set_xticks(x)
    axs[1].set_xticklabels(monthly_data.index)
    axs[1].set_title('Monthly Income and Expense Trends', fontsize=14)
    axs[1].set_xlabel('Month', fontsize=12)
    axs[1].set_ylabel('Amount', fontsize=12)
    axs[1].legend()
    axs[1].tick_params(axis='x', rotation=45)

    income_expense_summary = data.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)
    income_expense_summary['Savings'] = income_expense_summary['Income'] + income_expense_summary['Expense']
    income_expense_summary = income_expense_summary.fillna(0)

    table_data = income_expense_summary[['Income', 'Expense', 'Savings']].reset_index()

    axs[2].axis('off')
    axs[2].table(cellText=table_data.values,
                 colLabels=['Month', 'Income', 'Expense', 'Savings'],
                 cellLoc='center',
                 loc='center',
                 colColours=['#f1f1f1'] * 4)

    axs[2].set_title('Income, Expense, and Savings Summary by Month', fontsize=14)
    plt.tight_layout()
    plt.savefig('data/combined_analysis.png', format='png', dpi=300)