from datetime import datetime, date
from collections import defaultdict
from math import ceil

# -----------------------------
# Helpers
# -----------------------------
def parse_date(date_str, fmt="%B %d, %Y"):
    """Parse a date string into datetime, return None if invalid."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, fmt)
    except (ValueError, TypeError):
        return None

def format_date(date_obj, fmt="%B %d, %Y"):
    """Format datetime/date object into string, return empty if invalid."""
    if isinstance(date_obj, (datetime, date)):
        return date_obj.strftime(fmt)
    return ""

def paginate(items, page, per_page=10):
    """Return paginated slice and total pages, clamping page to valid range."""
    total_items = len(items)
    total_pages = max(1, ceil(total_items / per_page))

    # Clamp page number
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages

def aggregate_data(expenses):
    """
    Aggregate totals, categories, and monthly chart data in one pass.
    Works with SQLAlchemy Expense objects.
    """
    total = 0.0
    categories = defaultdict(float)
    monthly_totals = defaultdict(lambda: {"Savings": 0.0, "Spending": 0.0})

    for exp in expenses:
        # Defensive checks
        if not exp or exp.amount is None or not exp.category or not exp.type or not exp.date:
            continue

        amount = float(exp.amount)
        total += amount
        categories[exp.category] += amount

        month_label = exp.date.strftime("%b %Y")
        monthly_totals[month_label][exp.type] += amount

    # Sort months chronologically
    months = sorted(monthly_totals.keys(), key=lambda m: datetime.strptime(m, "%b %Y"))
    savings_data = [monthly_totals[m]["Savings"] for m in months]
    spending_data = [monthly_totals[m]["Spending"] for m in months]

    return total, dict(categories), months, savings_data, spending_data