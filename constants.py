"""
Constants and enums.

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


METRIC_CONSTANTS = {
    Metric.REVENUE: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        } 
    },
    Metric.GROSS_PROFIT: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        }
    },
    Metric.OPERATING_EXPENSES: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        }
    },
    Metric.NET_PROFIT: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        }
    },
    Metric.GROSS_PROFIT_RATIO: {
        "format": {
            "axis": ".0%",
            "tooltip": ".2%"
        }
    },
    Metric.OPERATING_EXPENSE_RATIO: {
        "format": {
            "axis": ".0%",
            "tooltip": ".2%"
        }
    }
}