from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from config import CATEGORY_OPTIONS
from utils import parse_date, format_date, paginate, aggregate_data  # keep only non‑JSON helpers
from flask_sqlalchemy import SQLAlchemy

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
        return f"<Expense {self.description} ₱{self.amount:.2f}>"

with app.app_context():
    db.create_all()

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()

    # Aggregations
    total, categories, months, savings_data, spending_data = aggregate_data(expenses)

    # Pagination
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
        total_pages=total_pages
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_expense = Expense(
            description=request.form["description"],
            category=request.form["category"],
            type=request.form["type"],
            amount=float(request.form["amount"]),
            date=datetime.strptime(request.form["date"], "%Y-%m-%d")
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
        expense.date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        expense.type = request.form["type"]
        expense.category = request.form["category"]
        expense.amount = float(request.form["amount"])
        expense.description = request.form["description"]
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
    Expense.query.delete()
    db.session.commit()
    return redirect(url_for("index"))

@app.template_filter("datetimeformat")
def datetimeformat(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return value

if __name__ == "__main__":
    app.run(debug=True)