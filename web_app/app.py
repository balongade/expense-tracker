from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid
from config import CATEGORY_OPTIONS
from utils import (
    load_expenses,
    save_expenses,
    parse_date,
    format_date,
    paginate,
    aggregate_data
)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    expenses = load_expenses()

    # Sort by Date (newest first)
    expenses.sort(
        key=lambda exp: parse_date(exp["Date"]) or datetime.min,
        reverse=True
    )

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
        expense = {
            "id": str(uuid.uuid4()),
            "Amount": float(request.form["amount"]),
            "Category": request.form["category"],
            "Description": request.form["description"],
            "Date": format_date(datetime.strptime(request.form["date"], "%Y-%m-%d")),
            "Type": request.form["type"]
        }
        expenses = load_expenses()
        expenses.append(expense)
        save_expenses(expenses)
        return redirect(url_for("index"))

    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("add.html", today=today, category_options=CATEGORY_OPTIONS)

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    expenses = load_expenses()
    for exp in expenses:
        if exp["id"] == id:
            if request.method == "POST":
                exp.update({
                    "Date": format_date(datetime.strptime(request.form["date"], "%Y-%m-%d")),
                    "Category": request.form["category"],
                    "Amount": float(request.form["amount"]),
                    "Description": request.form["description"],
                    "Type": request.form["type"]
                })
                save_expenses(expenses)
                return redirect(url_for("index"))
            return render_template("edit.html", expense=exp, category_options=CATEGORY_OPTIONS)
    return redirect(url_for("index"))

@app.template_filter("datetimeformat")
def datetimeformat(value):
    dt = parse_date(value)
    return dt.strftime("%Y-%m-%d") if dt else value

@app.route("/delete/<id>")
def delete(id):
    expenses = [exp for exp in load_expenses() if exp["id"] != id]
    save_expenses(expenses)
    return redirect(url_for("index"))

@app.route("/delete_all")
def delete_all():
    save_expenses([])  # overwrite with empty list
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)