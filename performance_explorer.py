from datetime import datetime, timedelta
from typing import Literal

import streamlit as st
import polars as pl
import altair as alt

import utils
from enums import Metric


# =======================
# Constants
# =======================
CHART_SETTINGS = {
    Metric.REVENUE: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        "scale": alt.Scale()   
    },
    Metric.GROSS_PROFIT: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        # "scale": alt.Scale() 
    },
    Metric.OPERATING_EXPENSES: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        # "scale": alt.Scale() 
    },
    Metric.NET_PROFIT: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        # "scale": alt.Scale()
    },
    Metric.GROSS_PROFIT_RATIO: {
        "format": {
            "axis": ".0%",
            "tooltip": ".2%"
        },
        # "scale": alt.Scale(domain=[0, 1])
    },
    Metric.OPERATING_EXPENSE_RATIO: {
        "format": {
            "axis": ".0%",
            "tooltip": ".2%"
        },
        # "scale": alt.Scale(domain=[0, 1])
    }
}

# =======================
# Functions
# =======================
# @st.cache_data(show_spinner=False)
def fetch_data():
    return pl.read_csv(
        "data/performance_metrics.csv",
        schema_overrides={"period": pl.Date}
    ).sort("period")


def performance_explorer_section(df: pl.DataFrame, metric_selection: Metric):
    df = df.filter(pl.col("metric").str.to_lowercase() == metric_selection.value.lower())
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(
            "yearmonth(period):T",
            title=None,
            axis=alt.Axis(
                format="%B %Y",
                labelAngle=-45,
                labelAlign="right",
                labelOverlap=False
            ),
        ),
        y=alt.Y(
            "value:Q",
            title=None,
            axis=alt.Axis(format=CHART_SETTINGS[metric_selection]["format"]["axis"]),
            # scale=CHART_SETTINGS[metric_selection]["scale"]
        ),
        tooltip=[
            alt.Tooltip("period:T", title="Period", format="%B %Y"),
            alt.Tooltip("value:Q", title=metric_selection.value, format=CHART_SETTINGS[metric_selection]["format"]["tooltip"])
        ]
    )

    with center.container(border=True):
        st.altair_chart(chart)


# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Performance explorer | Executive Portal",
    layout="wide"
)
left, center, right = st.columns([1, 5, 1])
center.header(":material/explore: Performance explorer")
left_center, center_center, right_center = center.columns(3)

df = fetch_data()

# period_options = df["period"].unique().to_list()
# period_selection = left_center.selectbox(
#     label="Period",
#     options=reversed(period_options),
#     index=0,
#     format_func=lambda x: datetime.strftime(x, "%B %Y")
# )

metric_selection = left_center.selectbox(
    label="Metric",
    options=list(Metric),
    format_func=lambda x: x.value
)

performance_explorer_section(df, metric_selection)