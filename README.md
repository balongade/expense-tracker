# 💰 Expense Tracker

A simple, responsive expense tracking web app built with Flask. Add, edit, delete, and visualize your monthly savings and spending — all in one place.

## 🚀 Features

- Add, edit, delete and visualize expenses
- Dynamic category selection based on type (Savings or Spending)
- Monthly line chart using Chart.js with percentage breakdowns
- Monthly total Table per Category
- Pagination with continuous row numbering
- Clean, responsive Bootstrap layout
- Modular codebase with `utils.py` and `config.py`

## 🛠️ Tech Stack

- Python 3.11
- Flask
- Bootstrap 5
- Chart.js
- Jinja2 templates

## 📦 Project Structure

```
expense-tracker/
├── app.py
├── utils.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── Procfile
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   └── edit.html
│
├── static/
│   ├── style.css
│   └── app.js
```

## ⚙️ Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/balongade/expense-tracker.git
   cd expense-tracker/
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Visit `http://127.0.0.1:5000` in your browser.

## 📄 License

This project is open-source under the MIT License.
