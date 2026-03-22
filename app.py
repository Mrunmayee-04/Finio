from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Account, Category, Transaction, Budget
from sqlalchemy import func
from datetime import datetime

# ── App Configuration ──────────────────────────────────────────
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'finio_secret_key'
db.init_app(app)

# ══════════════════════════════════════════════════════════════
# ROUTE 1 — Dashboard (Q1, Q2, Q3, Q4)
# ══════════════════════════════════════════════════════════════
@app.route('/')
def dashboard():
    # Q1: Total income across all transactions
    total_income = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == 'income').scalar() or 0

    # Q2: Total expenses across all transactions
    total_expense = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == 'expense').scalar() or 0

    # Q3: Total number of transactions
    txn_count = Transaction.query.count()

    # Q4: Latest 5 transactions with account and category name (JOIN)
    recent = db.session.query(Transaction, Account.name, Category.name)\
        .join(Account,  Transaction.account_id  == Account.id)\
        .join(Category, Transaction.category_id == Category.id)\
        .order_by(Transaction.date.desc()).limit(5).all()

    balance = total_income - total_expense
    return render_template('dashboard.html',
        total_income=total_income,
        total_expense=total_expense,
        txn_count=txn_count,
        recent=recent,
        balance=balance)

# ══════════════════════════════════════════════════════════════
# ROUTE 2 — All Transactions (Q5)
# ══════════════════════════════════════════════════════════════
@app.route('/transactions')
def transactions():
    # Q5: All transactions joined with account name and category name
    txns = db.session.query(Transaction, Account.name, Category.name)\
        .join(Account,  Transaction.account_id  == Account.id)\
        .join(Category, Transaction.category_id == Category.id)\
        .order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', txns=txns)

# ══════════════════════════════════════════════════════════════
# ROUTE 3 — Add Transaction (Q6, Q7)
# ══════════════════════════════════════════════════════════════
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        new_txn = Transaction(
            account_id  = int(request.form['account_id']),
            category_id = int(request.form['category_id']),
            amount      = float(request.form['amount']),
            description = request.form['description'],
            date        = datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            type        = request.form['type']
        )
        db.session.add(new_txn)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))

    # Q6: Fetch all accounts for dropdown
    accounts = Account.query.order_by(Account.name).all()
    # Q7: Fetch all categories for dropdown
    cats = Category.query.order_by(Category.name).all()
    return render_template('add.html', accounts=accounts, cats=cats)

# ══════════════════════════════════════════════════════════════
# ROUTE 4 — Delete Transaction (Q8)
# ══════════════════════════════════════════════════════════════
@app.route('/delete/<int:id>')
def delete_transaction(id):
    # Q8: Delete a specific transaction by its primary key
    txn = Transaction.query.get_or_404(id)
    db.session.delete(txn)
    db.session.commit()
    flash('Transaction deleted!', 'danger')
    return redirect(url_for('transactions'))

# ══════════════════════════════════════════════════════════════
# ROUTE 5 — All Accounts (Q9)
# ══════════════════════════════════════════════════════════════
@app.route('/accounts')
def accounts():
    # Q9: All accounts ordered by type
    all_accounts = Account.query.order_by(Account.type).all()
    return render_template('accounts.html', accounts=all_accounts)

# ══════════════════════════════════════════════════════════════
# ROUTE 6 — Edit Account Balance (Q20)
# ══════════════════════════════════════════════════════════════
@app.route('/account/edit/<int:aid>', methods=['POST'])
def edit_account(aid):
    # Q20: Update the balance of a specific account
    a = Account.query.get_or_404(aid)
    a.balance = float(request.form['balance'])
    db.session.commit()
    flash(f'{a.name} balance updated!', 'success')
    return redirect(url_for('accounts'))

# ══════════════════════════════════════════════════════════════
# ROUTE 7 — Budgets (Q10)
# ══════════════════════════════════════════════════════════════
@app.route('/budgets')
def budgets():
    # Q10: All budgets joined with category name
    all_budgets = db.session.query(Budget, Category.name)\
        .join(Category, Budget.category_id == Category.id)\
        .order_by(Budget.month.desc()).all()
    return render_template('budgets.html', budgets=all_budgets)

# ══════════════════════════════════════════════════════════════
# ROUTE 8 — Edit Budget (Q11)
# ══════════════════════════════════════════════════════════════
@app.route('/budget/edit/<int:bid>', methods=['POST'])
def edit_budget(bid):
    # Q11: Update the limit amount of a specific budget
    b = Budget.query.get_or_404(bid)
    b.limit_amount = float(request.form['limit_amount'])
    db.session.commit()
    flash('Budget updated!', 'success')
    return redirect(url_for('budgets'))

# ══════════════════════════════════════════════════════════════
# ROUTE 9 — Reports (Q12–Q17)
# ══════════════════════════════════════════════════════════════
@app.route('/reports')
def reports():
    # Q12: Total expense grouped by category
    by_cat = db.session.query(Category.name, func.sum(Transaction.amount))\
        .join(Transaction, Category.id == Transaction.category_id)\
        .filter(Transaction.type == 'expense')\
        .group_by(Category.name).all()

    # Q13: Monthly totals grouped by month
    monthly = db.session.query(
        func.strftime('%Y-%m', Transaction.date),
        func.sum(Transaction.amount)
    ).group_by(func.strftime('%Y-%m', Transaction.date)).all()

    # Q14: Average transaction amount
    avg_amt = round(db.session.query(
        func.avg(Transaction.amount)).scalar() or 0, 2)

    # Q15: Maximum single expense
    max_exp = db.session.query(func.max(Transaction.amount))\
        .filter(Transaction.type == 'expense').scalar() or 0

    # Q16: Minimum single expense
    min_exp = db.session.query(func.min(Transaction.amount))\
        .filter(Transaction.type == 'expense').scalar() or 0

    # Q17: Total balance across all accounts
    total_balance = db.session.query(
        func.sum(Account.balance)).scalar() or 0

    # Q18: Expense grouped by account (which account spends most)
    by_account = db.session.query(Account.name, func.sum(Transaction.amount))\
        .join(Transaction, Account.id == Transaction.account_id)\
        .filter(Transaction.type == 'expense')\
        .group_by(Account.name).all()

    return render_template('reports.html',
        by_cat=by_cat,
        monthly=monthly,
        avg_amt=avg_amt,
        max_exp=max_exp,
        min_exp=min_exp,
        total_balance=total_balance,
        by_account=by_account)

# ══════════════════════════════════════════════════════════════
# ROUTE 10 — Search Transactions (Q19)
# ══════════════════════════════════════════════════════════════
@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    results = []
    if keyword:
        # Q19: Search transactions by description using LIKE
        results = db.session.query(Transaction, Account.name, Category.name)\
            .join(Account,  Transaction.account_id  == Account.id)\
            .join(Category, Transaction.category_id == Category.id)\
            .filter(Transaction.description.like(f'%{keyword}%')).all()
    return render_template('search.html', results=results, keyword=keyword)

# ── Run ────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)