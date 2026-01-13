"""
Enums.

Author: Yakir Havin
"""


from enum import Enum


class FinancialCategory(Enum):
    REVENUE = "Revenue"
    COST_OF_GOODS_SOLD = "Cost of Goods Sold"
    OPERATING_EXPENSES = "Operating Expenses"


class Metric(Enum):
    REVENUE = "Revenue"
    GROSS_PROFIT = "Gross Profit"
    OPERATING_EXPENSES = "Operating Expenses"
    NET_PROFIT = "Net Profit"
    GROSS_PROFIT_RATIO = "Gross Profit Ratio"
    OPERATING_EXPENSE_RATIO = "Operating Expense Ratio"