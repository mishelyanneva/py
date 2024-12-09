

def classify_transaction(description, amount):
    """
    Classifies a transaction as Income or Expense with subcategories based on keywords.

    Args:
        description (str): The description of the transaction.
        amount (float): The transaction amount.

    Returns:
        tuple: (category, subcategory)
    """
    description = description.lower()  # Normalize text
    if amount > 0:
        # Income classification
        if 'salary' in description or 'payroll' in description:
            subcategory = 'Salary'
        elif 'bonus' in description or 'commission' in description:
            subcategory = 'Bonus/Commission'
        elif 'refund' in description:
            subcategory = 'Refund'
        else:
            subcategory = 'Other Income'
        category = 'Income'
    else:

        if 'rent' in description or 'lease' in description:
            subcategory = 'Rent'
        elif 'food' in description or 'restaurant' in description or 'groceries' in description:
            subcategory = 'Food'
        elif 'travel' in description or 'transport' in description:
            subcategory = 'Travel'
        elif 'utility' in description or 'electricity' in description or 'water' in description:
            subcategory = 'Utilities'
        elif 'shopping' in description or 'clothes' in description:
            subcategory = 'Shopping'
        else:
            subcategory = 'Other Expense'
        category = 'Expense'

    return category, subcategory
