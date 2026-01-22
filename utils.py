"""
Utility functions.

Author: Yakir Havin
"""


import streamlit as st
import polars as pl


def calculate_category_total(df: pl.DataFrame, category: str, value_column: str="activity"):
    """SUMIF on a DataFrame (category is case-insensitive)."""
    return df.filter(pl.col("category").str.to_lowercase() == category.lower()).select(pl.col(value_column).sum()).item()


def highlight_subtotal_row(row: pl.Series, index: str, highlight_rows: list[str], highlight_color: str="#f5f5f5") -> list[str]:
    """Apply shading to a subtotal row in a DataFrame."""
    if row[index] in highlight_rows:
        return [f"background-color: {highlight_color};"] * len(row)
    else:
        return [f'background-color: {st.get_option("theme.backgroundColor")}'] * len(row)
    
    
def calculate_dataframe_height(rows, height_per_row=35, extra=3):
    """
    Calculate height parameter for DataFrames.
    Default value of extra is 3 to allow for borders.
    Forum thread: https://discuss.streamlit.io/t/st-dataframe-controlling-the-height-threshold-for-scolling/31769/3
    """
    return (rows * height_per_row) + extra