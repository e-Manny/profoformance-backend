import math
import numpy_financial as npf
def cashflow(propertyName, purchasePrice, purchaseClosingCosts, renovations, valueGrowthRate, rent, rentGrowthRate, propertyTax, insurance, maintenance, propertyMgmt, otherOpEx, opExGrowthRate, capEx, capExGrowthRate, loanAmount, interestRate, amortization, holdingPeriod, saleClosingCosts):
  responseDict = {"totalMonths":holdingPeriod,
                  "propertyName": propertyName,
                  "months":[]}
  payedPrincipal = 0
  for month in range(holdingPeriod + 1):
    monthCF = {}
    if month == 0:
      monthCF["month"] = "Acquisition"
      monthCF["year"] = "Acquisition"
      monthCF["rent"] = 0
      monthCF["taxes"] = 0
      monthCF["insurance"] = 0
      monthCF["maintenance"] = 0
      monthCF["management"] = 0
      monthCF["other"] = 0
      monthCF["noi"] = 0
      monthCF["capEx"] = 0
      monthCF["purchase"] = int(-1 * purchasePrice)
      monthCF["closingCosts"] = int(-1 * purchaseClosingCosts)
      monthCF["initialRenovations"] = int(-1 * renovations)
      monthCF["principal"] = 0
      monthCF["interest"] = 0
      monthCF["loanProceeds"] = int(loanAmount)
    else:
      monthCF["month"] = month
      monthCF["year"] = math.ceil(month / 12)
      monthCF["rent"] = int((rent/12)*((1+(rentGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["taxes"] = int((propertyTax/12)*((1+(opExGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["insurance"] = int((insurance/12)*((1+(opExGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["maintenance"] = int((maintenance/12)*((1+(opExGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["management"] = int((propertyMgmt/12)*((1+(opExGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["other"] = int((otherOpEx/12)*((1+(opExGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["noi"] = monthCF["rent"] - monthCF["taxes"] - monthCF["insurance"] - monthCF["maintenance"] - monthCF["other"]
      monthCF["capEx"] = int((capEx/12)*((1+(capExGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["purchase"] = 0
      monthCF["initialRenovations"] = 0
      monthCF["closingCosts"] = 0
      monthCF["principal"] = -1 * npf.ppmt((interestRate/100)/12, month, amortization * 12, loanAmount)
      payedPrincipal -= monthCF["principal"]
      monthCF["principal"] = int(monthCF["principal"])
      monthCF["interest"] = int(-1 * npf.ipmt((interestRate/100)/12, month, amortization * 12, loanAmount))
      monthCF["loanProceeds"] = 0    
    if month != holdingPeriod:
      monthCF["saleProceeds"] = 0
      monthCF["saleCost"] = 0
      monthCF["loanPayoff"] = 0
    else:
      monthCF["saleProceeds"] = int((purchasePrice)*((1+(valueGrowthRate/100))**(math.ceil(month / 12)-1)))
      monthCF["saleCost"] = int(-1 * saleClosingCosts)
      monthCF["loanPayoff"] = int(-1 * (loanAmount + payedPrincipal))
    monthCF["cfbds"] = int(monthCF["noi"] - monthCF["capEx"])
    monthCF["cfads"] = int(monthCF["cfbds"] - monthCF["principal"] - monthCF["interest"])
    monthCF["unleveredCF"] = int(monthCF["cfbds"] + monthCF["purchase"] + monthCF["closingCosts"] + monthCF["saleProceeds"] + monthCF["saleCost"] + monthCF["initialRenovations"])
    monthCF["totalLeveredCF"] = int(monthCF["cfads"] + monthCF["purchase"] + + monthCF["closingCosts"] + monthCF["saleProceeds"] + monthCF["saleCost"] + monthCF["loanProceeds"] + monthCF["loanPayoff"] + monthCF["initialRenovations"])
    responseDict["months"].append(monthCF)
  return responseDict

# print(npf.ipmt((4/100)/12, 60, 30 * 12, 3000000))
print(cashflow("123 Main St", 5000000, 50000, 0, 0, 300000, 4, 0, 0, 0, 0, 0, 0, 5000, 3, 3000000, 4, 30, 60, 140383))
# print(cashflow(propertyName, purchasePrice, purchaseClosingCosts, renovations, 
# valueGrowthRate, rent, rentGrowthRate, propertyTax, insurance, maintenance, propertyMgmt, 
# otherOpEx, opExGrowthRate, capEx, capExGrowthRate, loanAmount, interestRate, amortization, holdingPeriod, saleClosingCosts))



