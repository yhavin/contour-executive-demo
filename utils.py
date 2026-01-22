"""
Utility functions.

Author: Yakir Havin
"""


import polars as pl


def calculate_category_total(df: pl.DataFrame, category: str, value_column: str="activity"):
    """SUMIF on a DataFrame (category is case-insensitive)."""
    return df.filter(pl.col("category").str.to_lowercase() == category.lower()).select(pl.col(value_column).sum()).item()