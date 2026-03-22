from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)   # e.g. HDFC Savings
    type          = db.Column(db.String(20),  nullable=False)   # bank / cash / credit / upi
    balance       = db.Column(db.Float,       default=0.0)      # current balance
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    # one account can have many transactions
    transactions  = db.relationship('Transaction', backref='account', lazy=True)


class Category(db.Model):
    __tablename__ = 'categories'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(50),  nullable=False)   # e.g. Food, Rent, Salary
    type          = db.Column(db.String(10),  nullable=False)   # income or expense

    # one category can have many transactions and budgets
    transactions  = db.relationship('Transaction', backref='category', lazy=True)
    budgets       = db.relationship('Budget',      backref='category', lazy=True)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id            = db.Column(db.Integer, primary_key=True)
    account_id    = db.Column(db.Integer, db.ForeignKey('accounts.id'),   nullable=False)
    category_id   = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount        = db.Column(db.Float,   nullable=False)
    description   = db.Column(db.String(200))
    date          = db.Column(db.Date,    nullable=False)
    type          = db.Column(db.String(10), nullable=False)    # income or expense


class Budget(db.Model):
    __tablename__ = 'budgets'
    id            = db.Column(db.Integer, primary_key=True)
    category_id   = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    limit_amount  = db.Column(db.Float,   nullable=False)
    month         = db.Column(db.String(7), nullable=False)     # format: "2024-06"