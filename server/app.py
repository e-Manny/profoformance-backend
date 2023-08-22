from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from config import ApplicationConfig
from models import db, User, Property
from cashflow import cashflow

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5173"}}, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
  db.create_all()

@app.route("/@me")
def get_current_user():
  user_id = session.get("user_id")

  if not user_id:
    return jsonify({"error":"Unauthorized"}), 401
  
  user = User.query.filter_by(id=user_id).first()
  properties = Property.query.filter_by(userID=user_id)
  propertyNames = []
  propertyIDs = []
  for property in properties:
     propertyNames.append(property.propertyName)
     propertyIDs.append(property.id)

  return jsonify({
     "id": user.id,
     "propertyNames": propertyNames,
     "propertyIDs": propertyIDs
  })

@app.route("/register", methods=["POST"])
def register_user():
  email = request.json["email"]
  password = request.json["password"]

  user_exists = User.query.filter_by(email = email).first() is not None
  if user_exists:
    return jsonify({"error": "User already exists"}), 409

  hashed_password = bcrypt.generate_password_hash(password)
  new_user = User(email=email, password=hashed_password)
  db.session.add(new_user)
  db.session.commit()
  return jsonify({
     "id": new_user.id,
     "email": new_user.email
  })

@app.route("/login", methods=["POST"])
def login_user():
  email = request.json["email"]
  password = request.json["password"]

  user = User.query.filter_by(email = email).first()
  if user is None:
    return jsonify({"error":"no username exists"}), 401
  if not bcrypt.check_password_hash(user.password, password):
    return jsonify({"error":"wrong password"}), 401
  session["user_id"] = user.id
  print(session)
  return jsonify({
     "id": user.id,
     "email": user.email
  }), 200

@app.route("/logout", methods=["POST"])
def logout_user():
    if "user_id" in session:
        session.pop("user_id")
        return jsonify({"message": "Logged out successfully"}), 200
    else:
        return jsonify({"error": "Not logged in"}), 401

@app.route("/addproperty", methods=["POST"])
def add_property():
  user_id = session.get("user_id")

  if not user_id:
    return jsonify({"error":"Unauthorized"}), 401
  userID = session.get("user_id")
  propertyName = request.json["propertyName"]
  yearBuilt = request.json["yearBuilt"]
  address = request.json["address"]
  city = request.json["city"]
  zipCode = request.json["zipCode"]
  state = request.json["state"]
  purchasePrice = request.json["purchasePrice"]
  purchaseClosingCosts = request.json["purchaseClosingCosts"]
  renovationCosts = request.json["renovationCosts"]
  valueGrowthRate = request.json["valueGrowthRate"]
  anualRentalIncome = request.json["anualRentalIncome"]
  rentGrowthRate = request.json["rentGrowthRate"]
  capEx = request.json["capEx"]
  capExGrowthRate = request.json["capExGrowthRate"]
  propertyTax = request.json["propertyTax"]
  insurance = request.json["insurance"]
  maintenance = request.json["maintenance"]
  propertyManagement = request.json["propertyManagement"]
  otherExpense = request.json["otherExpense"]
  expenseGrowth = request.json["expenseGrowth"]
  loanAmount = request.json["loanAmount"]
  interestRate = request.json["interestRate"]
  amortizationYears = request.json["amortizationYears"]
  holdingPeriod = request.json["holdingPeriod"]
  saleClosingCosts = request.json["saleClosingCosts"]

  new_property = Property(userID = userID, propertyName = propertyName, yearBuilt = yearBuilt, address = address, city = city, zipCode = zipCode, state = state, purchasePrice = purchasePrice, purchaseClosingCosts = purchaseClosingCosts, renovationCosts = renovationCosts, valueGrowthRate = valueGrowthRate, anualRentalIncome = anualRentalIncome, rentGrowthRate = rentGrowthRate, capEx = capEx, capExGrowthRate = capExGrowthRate, loanAmount = loanAmount, interestRate = interestRate, amortizationYears = amortizationYears, holdingPeriod = holdingPeriod, saleClosingCosts = saleClosingCosts, propertyTax = propertyTax, insurance = insurance, maintenance = maintenance, propertyManagement = propertyManagement, otherExpense = otherExpense, expenseGrowth = expenseGrowth)

  db.session.add(new_property)
  db.session.commit()
  return jsonify({
     "id": new_property.id
  })

@app.route("/property", methods=["POST"])
def get_property_cashflow():
  user_id = session.get("user_id")

  if not user_id:
    return jsonify({"error":"Unauthorized"}), 401

  prop = Property.query.filter_by(id=request.json["id"]).first()
  propertyName = prop.propertyName
  purchasePrice = prop.purchasePrice
  purchaseClosingCosts = prop.purchaseClosingCosts
  renovationCosts = prop.renovationCosts
  valueGrowthRate = prop.valueGrowthRate
  anualRentalIncome = prop.anualRentalIncome
  rentGrowthRate = prop.rentGrowthRate
  propertyTax = prop.propertyTax
  insurance = prop.insurance
  maintenance = prop.maintenance
  propertyManagement = prop.propertyManagement
  otherExpense = prop.otherExpense
  expenseGrowth = prop.expenseGrowth
  capEx = prop.capEx
  capExGrowthRate = prop.capExGrowthRate
  loanAmount = prop.loanAmount
  interestRate = prop.interestRate
  amortizationYears = prop.amortizationYears
  holdingPeriod = prop.holdingPeriod
  saleClosingCosts = prop.saleClosingCosts
  propertyCashFlow = cashflow(propertyName, purchasePrice, purchaseClosingCosts, renovationCosts, valueGrowthRate, anualRentalIncome, rentGrowthRate, propertyTax, insurance, maintenance, propertyManagement, otherExpense, expenseGrowth, capEx, capExGrowthRate, loanAmount, interestRate, amortizationYears, holdingPeriod, saleClosingCosts)
  return jsonify({
     "cashflow": propertyCashFlow
    #  "cashflow": propertyCashFlow
  })

if __name__ == "__main__":
    app.run(debug=True)