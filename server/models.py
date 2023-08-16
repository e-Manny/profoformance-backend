from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
  return uuid4().hex

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.String(32), primary_key = True, unique = True, default = get_uuid )
  email = db.Column(db.String(345), unique=True)
  password = db.Column(db.Text, nullable=False)

class Property(db.Model):
  __tablename__ = "properties"
  # Property details
  id = db.Column(db.String(32), primary_key = True, unique = True, default = get_uuid )
  userID = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False, unique = False)
  propertyName = db.Column(db.String(32), nullable=False)
  yearBuilt = db.Column(db.Integer, nullable=False)
  address = db.Column(db.String(50), nullable=False)
  state = db.Column(db.String(50), nullable=False)
  city = db.Column(db.String(50), nullable=False)
  zipCode = db.Column(db.Integer, nullable=False)
  # Acquisition details
  purchasePrice = db.Column(db.Integer, nullable=False)
  purchaseClosingCosts = db.Column(db.Integer, nullable=False)
  renovationCosts = db.Column(db.Integer, nullable=False)
  valueGrowthRate = db.Column(db.Float, nullable=False)
  #Rental income
  anualRentalIncome = db.Column(db.Integer, nullable=False)
  rentGrowthRate = db.Column(db.Float, nullable=False)
  #Operating expenses
  propertyTax = db.Column(db.Integer, nullable=False)
  insurance = db.Column(db.Integer, nullable=False)
  maintenance = db.Column(db.Integer, nullable=False)
  propertyManagement = db.Column(db.Integer, nullable=False)
  otherExpense = db.Column(db.Integer, nullable=False)
  expenseGrowth = db.Column(db.Float, nullable=False)
  #Capital expenses
  capEx = db.Column(db.Integer, nullable=False)
  capExGrowthRate = db.Column(db.Float, nullable=False)
  #Debt service
  loanAmount = db.Column(db.Integer, nullable=False)
  interestRate = db.Column(db.Float, nullable=False)
  amortizationYears = db.Column(db.Integer, nullable=False)
  #Disposition info
  holdingPeriod = db.Column(db.Integer, nullable=False)
  saleClosingCosts = db.Column(db.Integer, nullable=False)