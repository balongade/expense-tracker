from datetime import datetime
from collections import defaultdict
from math import ceil

# -----------------------------
# Helpers
# -----------------------------
def parse_date(date_str, fmt="%B %d, %Y"):
    """Safely parse a date string into datetime, return None if invalid."""
    try:
        return datetime.strptime(date_str, fmt)
    except Exception:
        return None

def format_date(date_obj, fmt="%B %d, %Y"):
    """Format datetime object into string."""
    return date_obj.strftime(fmt)

def paginate(items, page, per_page=10):
    """Return paginated slice and total pages."""
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = ceil(len(items) / per_page)
    return items[start:end], total_pages

def aggregate_data(expenses):
    """Aggregate totals, categories, and monthly chart data in one pass."""
    total = 0
    categories = defaultdict(float)
    monthly_totals = defaultdict(lambda: {"Savings": 0, "Spending": 0})

    for exp in expenses:
        amount = exp.amount
        total += amount
        categories[exp.category] += amount

        dt = exp.date
        if dt:
            month_label = dt.strftime("%b %Y")
            monthly_totals[month_label][exp.type] += amount

    months = sorted(monthly_totals.keys(), key=lambda m: datetime.strptime(m, "%b %Y"))
    savings_data = [monthly_totals[m]["Savings"] for m in months]
    spending_data = [monthly_totals[m]["Spending"] for m in months]

    return total, dict(categories), months, savings_data, spending_data