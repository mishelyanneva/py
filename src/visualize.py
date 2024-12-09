import pandas as pd
import matplotlib.pyplot as plt

def generate_report(data):

    return data.groupby(['Category', 'Subcategory'])['Amount'].sum().reset_index()

def create_summary_chart(data):

    summary = data.groupby('Category')['Amount'].sum().reset_index()
    colors = {'Income': 'green', 'Expense': 'red'}
    plt.bar(summary['Category'], summary['Amount'], color=summary['Category'].map(colors))
    plt.title('Income vs Expense')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.savefig('data/summary_chart.png')
    plt.close()
