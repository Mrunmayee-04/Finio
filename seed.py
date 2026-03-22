from app import app, db
from database import Account, Category, Transaction, Budget
from datetime import date

with app.app_context():
    db.drop_all()    # fresh start every time you run this
    db.create_all()  # creates all 4 tables

    # ── 20 Accounts ───────────────────────────────────────────
    # These are all the places where your money lives
    accounts = [
        Account(name="HDFC Savings",       type="bank",   balance=45000),
        Account(name="SBI Account",        type="bank",   balance=12000),
        Account(name="Cash Wallet",        type="cash",   balance=2500),
        Account(name="GPay UPI",           type="upi",    balance=1500),
        Account(name="PhonePe UPI",        type="upi",    balance=800),
        Account(name="HDFC Credit Card",   type="credit", balance=0),
        Account(name="SBI Credit Card",    type="credit", balance=0),
        Account(name="Paytm Wallet",       type="wallet", balance=300),
        Account(name="Amazon Pay",         type="wallet", balance=150),
        Account(name="Emergency Fund",     type="savings",balance=50000),
        Account(name="Fixed Deposit",      type="savings",balance=100000),
        Account(name="Zerodha",            type="investment", balance=25000),
        Account(name="Groww",              type="investment", balance=15000),
        Account(name="PPF Account",        type="savings",balance=75000),
        Account(name="Recurring Deposit",  type="savings",balance=20000),
        Account(name="Axis Bank",          type="bank",   balance=8000),
        Account(name="Kotak Account",      type="bank",   balance=5000),
        Account(name="ICICI Credit Card",  type="credit", balance=0),
        Account(name="Sodexo Card",        type="wallet", balance=2000),
        Account(name="Post Office Savings",type="savings",balance=30000),
    ]
    db.session.add_all(accounts)

    # ── 20 Categories ─────────────────────────────────────────
    # Labels for what the money was for
    categories = [
        Category(name="Salary",          type="income"),
        Category(name="Freelance",       type="income"),
        Category(name="Food",            type="expense"),
        Category(name="Rent",            type="expense"),
        Category(name="Transport",       type="expense"),
        Category(name="Medical",         type="expense"),
        Category(name="Shopping",        type="expense"),
        Category(name="Utilities",       type="expense"),
        Category(name="Entertainment",   type="expense"),
        Category(name="Education",       type="expense"),
        Category(name="Groceries",       type="expense"),
        Category(name="Fuel",            type="expense"),
        Category(name="Dining Out",      type="expense"),
        Category(name="Gym",             type="expense"),
        Category(name="Subscriptions",   type="expense"),
        Category(name="Insurance",       type="expense"),
        Category(name="Travel",          type="expense"),
        Category(name="Investment",      type="income"),
        Category(name="Cashback",        type="income"),
        Category(name="Gift",            type="income"),
    ]
    db.session.add_all(categories)
    db.session.commit()  # commit first so IDs exist for FK references

    # ── 20 Transactions ───────────────────────────────────────
    # Every money movement — realistic day to day life
    transactions = [
        Transaction(account_id=1,  category_id=1,  amount=52000, type="income",
                    description="Monthly salary — June",          date=date(2024,6,1)),
        Transaction(account_id=4,  category_id=3,  amount=320,   type="expense",
                    description="Lunch at office canteen",        date=date(2024,6,2)),
        Transaction(account_id=1,  category_id=4,  amount=12000, type="expense",
                    description="House rent — June",              date=date(2024,6,3)),
        Transaction(account_id=3,  category_id=11, amount=850,   type="expense",
                    description="Big Bazaar groceries",           date=date(2024,6,5)),
        Transaction(account_id=4,  category_id=5,  amount=200,   type="expense",
                    description="Auto rickshaw to office",        date=date(2024,6,6)),
        Transaction(account_id=2,  category_id=2,  amount=8000,  type="income",
                    description="Freelance logo design project",  date=date(2024,6,8)),
        Transaction(account_id=6,  category_id=7,  amount=3500,  type="expense",
                    description="Myntra clothing haul",           date=date(2024,6,10)),
        Transaction(account_id=1,  category_id=16, amount=5500,  type="expense",
                    description="LIC premium payment",            date=date(2024,6,11)),
        Transaction(account_id=4,  category_id=13, amount=1200,  type="expense",
                    description="Dinner at Social restaurant",    date=date(2024,6,13)),
        Transaction(account_id=3,  category_id=12, amount=2500,  type="expense",
                    description="Petrol for bike — full tank",    date=date(2024,6,15)),
        Transaction(account_id=1,  category_id=18, amount=5000,  type="income",
                    description="Groww mutual fund returns",      date=date(2024,6,16)),
        Transaction(account_id=8,  category_id=15, amount=199,   type="expense",
                    description="Netflix subscription",           date=date(2024,6,17)),
        Transaction(account_id=4,  category_id=8,  amount=1450,  type="expense",
                    description="Electricity bill — June",        date=date(2024,6,18)),
        Transaction(account_id=1,  category_id=10, amount=9000,  type="expense",
                    description="Coursera annual subscription",   date=date(2024,6,19)),
        Transaction(account_id=3,  category_id=14, amount=1200,  type="expense",
                    description="Cult.fit gym membership",        date=date(2024,6,20)),
        Transaction(account_id=1,  category_id=17, amount=15000, type="expense",
                    description="Goa trip — flights + hotel",     date=date(2024,6,21)),
        Transaction(account_id=6,  category_id=6,  amount=800,   type="expense",
                    description="Doctor consultation + medicines", date=date(2024,6,22)),
        Transaction(account_id=4,  category_id=19, amount=250,   type="income",
                    description="GPay cashback reward",           date=date(2024,6,23)),
        Transaction(account_id=3,  category_id=9,  amount=600,   type="expense",
                    description="BookMyShow — movie tickets",     date=date(2024,6,25)),
        Transaction(account_id=2,  category_id=20, amount=2000,  type="income",
                    description="Birthday gift from family",      date=date(2024,6,27)),
    ]
    db.session.add_all(transactions)

    # ── 20 Budgets ────────────────────────────────────────────
    # Your monthly spending limits per category
    budgets = [
        Budget(category_id=3,  limit_amount=2000,  month="2024-06"),  # Food
        Budget(category_id=4,  limit_amount=13000, month="2024-06"),  # Rent
        Budget(category_id=5,  limit_amount=1000,  month="2024-06"),  # Transport
        Budget(category_id=6,  limit_amount=1500,  month="2024-06"),  # Medical
        Budget(category_id=7,  limit_amount=3000,  month="2024-06"),  # Shopping
        Budget(category_id=8,  limit_amount=2000,  month="2024-06"),  # Utilities
        Budget(category_id=9,  limit_amount=800,   month="2024-06"),  # Entertainment
        Budget(category_id=10, limit_amount=10000, month="2024-06"),  # Education
        Budget(category_id=11, limit_amount=1500,  month="2024-06"),  # Groceries
        Budget(category_id=12, limit_amount=3000,  month="2024-06"),  # Fuel
        Budget(category_id=13, limit_amount=1500,  month="2024-06"),  # Dining Out
        Budget(category_id=14, limit_amount=1200,  month="2024-06"),  # Gym
        Budget(category_id=15, limit_amount=500,   month="2024-06"),  # Subscriptions
        Budget(category_id=16, limit_amount=6000,  month="2024-06"),  # Insurance
        Budget(category_id=17, limit_amount=20000, month="2024-06"),  # Travel
        Budget(category_id=3,  limit_amount=2000,  month="2024-07"),  # Food July
        Budget(category_id=4,  limit_amount=13000, month="2024-07"),  # Rent July
        Budget(category_id=5,  limit_amount=1000,  month="2024-07"),  # Transport July
        Budget(category_id=11, limit_amount=1500,  month="2024-07"),  # Groceries July
        Budget(category_id=17, limit_amount=10000, month="2024-07"),  # Travel July
    ]
    db.session.add_all(budgets)
    db.session.commit()

    print("✅ Finio database seeded successfully!")
    print(f"   Accounts:     {Account.query.count()}")
    print(f"   Categories:   {Category.query.count()}")
    print(f"   Transactions: {Transaction.query.count()}")
    print(f"   Budgets:      {Budget.query.count()}")