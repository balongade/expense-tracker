from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from config import CATEGORY_OPTIONS
from utils import paginate, aggregate_data
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from calendar import month_name

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Expense id={self.id} {self.description} ₱{self.amount:.2f}>"

with app.app_context():
    db.create_all()

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()

    # --- Existing Aggregations for Chart ---
    total, categories, months, savings_data, spending_data = aggregate_data(expenses)

    # --- New Aggregation for Table ---
    monthly_category_totals = defaultdict(lambda: defaultdict(float))
    for exp in expenses:
        month = month_name[exp.date.month]   # e.g. 1 → "January"
        monthly_category_totals[month][exp.category] += exp.amount

    # Prepare headers for table
    all_categories = sorted({
        cat for month in monthly_category_totals.values() for cat in month
    })
    table_months = sorted(
        monthly_category_totals.keys(),
        key=lambda m: list(month_name).index(m)
    )

    # --- Pagination ---
    page = int(request.args.get("page", 1))
    paginated_expenses, total_pages = paginate(expenses, page, per_page=10)

    return render_template(
        "index.html",
        expenses=paginated_expenses,
        total=total,
        categories=categories,
        months=months,
        savings_data=savings_data,
        spending_data=spending_data,
        page=page,
        total_pages=total_pages,
        monthly_category_totals=monthly_category_totals,
        all_categories=all_categories,
        table_months=table_months
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_expense = Expense(
            description=request.form.get("description", "").strip(),
            category=request.form.get("category", "").strip(),
            type=request.form.get("type", "").strip(),
            amount=float(request.form.get("amount", 0) or 0),
            date=datetime.strptime(request.form.get("date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for("index"))
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("add.html", today=today, category_options=CATEGORY_OPTIONS)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    expense = Expense.query.get_or_404(id)
    if request.method == "POST":
        expense.date = datetime.strptime(
            request.form.get("date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d"
        )
        expense.type = request.form.get("type", expense.type).strip()
        expense.category = request.form.get("category", expense.category).strip()
        expense.amount = float(request.form.get("amount", expense.amount) or 0)
        expense.description = request.form.get("description", expense.description).strip()
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", expense=expense, category_options=CATEGORY_OPTIONS)

@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete_all")
def delete_all():
    db.session.query(Expense).delete()
    db.session.commit()
    return redirect(url_for("index"))

@app.template_filter("datetimeformat")
def datetimeformat(value, fmt="%B %d, %Y"):
    try:
        return value.strftime(fmt)
    except Exception:
        return value

if __name__ == "__main__":
    app.run(debug=True)