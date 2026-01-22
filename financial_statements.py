from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import polars as pl

import utils
from constants import IncomeStatementCategory, BalanceSheetCategory


# =======================
# Functions
# =======================
# @st.cache_data(show_spinner=False)
def fetch_data():
    return pl.read_csv(
        "data/trial_balance.csv",
        schema_overrides={
            "period": pl.Date,
            "gl_account_code": pl.Utf8,
            "opening_balance": pl.Float64,
            "debit": pl.Float64,
            "credit": pl.Float64,
            "closing_balance": pl.Float64,
            "activity": pl.Float64
        }
    ).sort("period")


def income_statement_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    df = df.filter(
        (pl.col("period").is_between(from_period_selection, to_period_selection)) &
        (pl.col("gl_account_code").str.contains("^[4-9]"))  # P&L accounts only
    )

    df = df.pivot(
        on="period",
        index=["gl_account_code", "gl_account_description"],
        values="activity"
    )

    period_columns = [column for column in df.columns if column not in ["gl_account_code", "gl_account_description"]]

    revenue_accounts = df.filter(pl.col("gl_account_code").str.starts_with("4")).with_columns([pl.col(column) * -1 for column in period_columns])
    cost_of_goods_sold_accounts = df.filter(pl.col("gl_account_code").str.starts_with("5"))
    operating_expense_accounts = df.filter(pl.col("gl_account_code").str.contains("^[6-9]"))

    total_revenue = (revenue_accounts.select(period_columns).sum()).with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(IncomeStatementCategory.TOTAL_REVENUE.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    total_cost_of_goods_sold = cost_of_goods_sold_accounts.select(period_columns).sum().with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(IncomeStatementCategory.TOTAL_COST_OF_GOODS_SOLD.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    gross_profit = (total_revenue.select(period_columns) - total_cost_of_goods_sold.select(period_columns)).with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(IncomeStatementCategory.GROSS_PROFIT.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    total_operating_expenses = operating_expense_accounts.select(period_columns).sum().with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(IncomeStatementCategory.TOTAL_OPERATING_EXPENSES.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    net_profit = (gross_profit.select(period_columns) - total_operating_expenses.select(period_columns)).with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(IncomeStatementCategory.NET_PROFIT.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    df = pl.concat([
        revenue_accounts,
        total_revenue, 
        cost_of_goods_sold_accounts,
        total_cost_of_goods_sold, 
        gross_profit, 
        operating_expense_accounts,
        total_operating_expenses, 
        net_profit
    ])

    df = df.drop("gl_account_code")

    styled_df = df.to_pandas().style.apply(
        lambda row: utils.highlight_subtotal_row(row, "gl_account_description", [category.value for category in IncomeStatementCategory]), 
        axis=1
    )

    center.dataframe(
        styled_df,
        height=utils.calculate_dataframe_height(df.shape[0] + 1),
        width=min(150 * df.shape[1], 1200),
        column_config={
            "gl_account_description": "",
            **{column: st.column_config.NumberColumn(
                label=pl.Series([column]).str.to_datetime().dt.strftime("%b %Y").item(),
                format="accounting"
            ) for column in period_columns}
        },
        hide_index=True
    )


def balance_sheet_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    df = df.filter(
        (pl.col("period").is_between(from_period_selection, to_period_selection)) &
        (pl.col("gl_account_code").str.contains("^[1-3]"))  # Balance sheet accounts only
    )

    df = df.pivot(
        on="period",
        index=["gl_account_code", "gl_account_description"],
        values="closing_balance"
    )

    period_columns = [column for column in df.columns if column not in ["gl_account_code", "gl_account_description"]]

    asset_accounts = df.filter(pl.col("gl_account_code").str.starts_with("1"))
    liability_accounts = df.filter(pl.col("gl_account_code").str.starts_with("2"))
    equity_accounts = df.filter(pl.col("gl_account_code").str.starts_with("3"))

    total_assets = (asset_accounts.select(period_columns).sum()).with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(BalanceSheetCategory.TOTAL_ASSETS.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    total_liabilities = (liability_accounts.select(period_columns).sum()).with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(BalanceSheetCategory.TOTAL_LIABILITIES.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    total_equity = (equity_accounts.select(period_columns).sum()).with_columns(
        pl.lit(None).alias("gl_account_code"),
        pl.lit(BalanceSheetCategory.TOTAL_EQUITY.value).alias("gl_account_description")
    ).select(["gl_account_code", "gl_account_description"] + period_columns)

    df = pl.concat([
        asset_accounts,
        total_assets,
        liability_accounts,
        total_liabilities,
        equity_accounts,
        total_equity
    ])

    df = df.drop("gl_account_code")

    styled_df = df.to_pandas().style.apply(
        lambda row: utils.highlight_subtotal_row(row, "gl_account_description", [category.value for category in BalanceSheetCategory]),
        axis=1
    )

    center.dataframe(
        styled_df,
        height=utils.calculate_dataframe_height(df.shape[0] + 1),
        width=min(150 * df.shape[1], 1200),
        column_config={
            "gl_account_description": "",
            **{column: st.column_config.NumberColumn(
                label=pl.Series([column]).str.to_datetime().dt.strftime("%b %Y").item(),
                format="accounting"
            ) for column in period_columns}
        },
        hide_index=True
    )


def cash_flow_statement_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    left_center.info("This statement has not been implemented yet.")


# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Financial statements | Executive Portal",
    layout="wide"
)

left, center, right = st.columns([1, 7, 1])
center.header(":material/article: Financial statements")

df = fetch_data()

financial_statement_selection = center.pills(
    label="Statement",
    options=["Income Statement", "Balance Sheet"],
    default="Income Statement"
)

left_center, center_center, right_center = center.columns(3)

period_options = df["period"].unique().to_list()
from_period_selection, to_period_selection = left_center.select_slider(
    label="Date range",
    options=(period_options),
    value=(period_options[-6], period_options[-1]),
    format_func=lambda x: datetime.strftime(x, "%B %Y")
)

if financial_statement_selection == "Income Statement":
    income_statement_section(df, from_period_selection, to_period_selection)
elif financial_statement_selection == "Balance Sheet":
    balance_sheet_section(df, from_period_selection, to_period_selection)
elif financial_statement_selection == "Cash Flow Statement":
    cash_flow_statement_section(df, from_period_selection, to_period_selection)

center.badge(f"Latest data: {datetime.now(tz=ZoneInfo("America/New_York")):%B %e, %Y}", color="grey")