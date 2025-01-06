def classify_transaction(description: str, amount: float) -> tuple:

    description = description.lower()  # Normalize text

    income_keywords = {
        'Salary': ['salary', 'payroll', 'wages'],
        'Bonus/Commission': ['bonus', 'commission', 'incentive'],
        'Refund': ['refund', 'rebate', 'reimbursement'],
        'Other Income': []  # Default category for unmatched incomes
    }

    expense_keywords = {
        'Rent': ['rent', 'lease'],
        'Food': ['food', 'restaurant', 'groceries', 'dining'],
        'Travel': ['travel', 'transport', 'flight', 'hotel'],
        'Utilities': ['utility', 'electricity', 'water', 'gas'],
        'Shopping': ['shopping', 'clothes', 'apparel', 'retail'],
        'Other Expense': []  # Default category for unmatched expenses
    }

    if amount > 0:  # Income classification
        category = 'Income'
        subcategory = next(
            (key for key, keywords in income_keywords.items() if any(kw in description for kw in keywords)),
            'Other Income'
        )
    else:  # Expense classification
        category = 'Expense'
        subcategory = next(
            (key for key, keywords in expense_keywords.items() if any(kw in description for kw in keywords)),
            'Other Expense'
        )

    return category, subcategory
