def classify_transaction(description: str, amount: float) -> tuple:

    description = description.lower()

    income_keywords = {
        'Salary': ['salary', 'payroll', 'wages','bonus', 'commission', 'incentive'],
        'Refund': ['refund', 'rebate', 'reimbursement'],
        'Other Income': []
    }

    expense_keywords = {
        'Rent': ['rent', 'lease', 'utility', 'electricity', 'water', 'gas'],
        'Food': ['food', 'restaurant', 'groceries', 'dining'],
        'Travel': ['travel', 'transport', 'flight', 'hotel'],
        'Shopping': ['shopping', 'clothes', 'apparel', 'retail'],
        'Other Expense': []
    }

    if amount > 0:
        category = 'Income'
        subcategory = next(
            (key for key, keywords in income_keywords.items()
             if any(kw in description for kw in keywords)),
            'Other Income'
        )
    else:
        category = 'Expense'
        subcategory = next(
            (key for key, keywords in expense_keywords.items()
             if any(kw in description for kw in keywords)),
            'Other Expense'
        )

    return category, subcategory
