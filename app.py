"""Streamlit app: historical demand patterns for bakery preparation planning."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from bakery_analysis import (
    DATA_FILE,
    TIME_WINDOWS,
    bakery_item_window_rates,
    dashboard_metrics,
    filter_day_type,
    hourly_transaction_rates,
    load_transactions,
)

# Project attribution for the individual submission.
TEAM_NAME = "Team 7"
STUDENT_NAME = "Chen ziye"

st.set_page_config(
    page_title="Bakery Preparation | Decision Dashboard",
    page_icon="🥐",
    layout="wide",
)

COLORS = {"ink": "#273E36", "green": "#347B6A", "light": "#D0E1D5", "ochre": "#D8985C"}

@st.cache_data(show_spinner=False)
def get_data():
    return load_transactions(DATA_FILE)


def plot_hourly(hourly, peak_hour):
    fig, ax = plt.subplots(figsize=(9.1, 3.25))
    hours = hourly.index.to_numpy()
    values = hourly.to_numpy()
    bar_colors = [COLORS["ochre"] if h == peak_hour else COLORS["light"] for h in hours]
    ax.bar(hours, values, color=bar_colors, edgecolor="none", width=0.72)
    ax.set_xticks(hours, [f"{h:02d}:00" for h in hours], fontsize=9)
    ax.set_ylabel("Avg transactions / recorded day", fontsize=9)
    ax.set_xlabel("Hour of day", fontsize=9)
    ax.set_ylim(0, max(values.max() * 1.15, 1))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="y", color="#DCE5DE", linestyle="-", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=1.2)
    return fig


def plot_product_windows(pivot):
    fig, ax = plt.subplots(figsize=(9.1, 3.55))
    if pivot.empty:
        ax.text(0.5, 0.5, "No matching bakery items", ha="center", va="center")
        ax.axis("off")
        return fig
    y = np.arange(len(pivot))
    width = 0.38
    ax.barh(y - width / 2, pivot[TIME_WINDOWS[0]].values,
            height=width, label="Morning (08–11)", color=COLORS["green"])
    ax.barh(y + width / 2, pivot[TIME_WINDOWS[1]].values,
            height=width, label="Afternoon (12–16)", color=COLORS["ochre"])
    ax.set_yticks(y, pivot.index, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Transactions containing item / recorded day", fontsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#DCE5DE", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.tight_layout(pad=1.2)
    return fig


st.title(f"🥐 {TEAM_NAME} | Bakery Preparation")
st.caption(f"Prepared by {STUDENT_NAME} · {TEAM_NAME}")
st.caption(
    "For a bakery store manager: decide **when** to prepare and **which baked goods** "
    "to prioritize, using historical transaction patterns."
)
st.info(
    "**Historical demonstration only.** This CSV covers Oct 30, 2016 to Apr 9, 2017 "
    "and is not connected to a live point-of-sale system."
)

try:
    data = get_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

selected_day_type = st.selectbox(
    "Compare demand for:",
    ["All days", "Weekday", "Weekend"],
    index=0,
    help="Use separate weekday or weekend history when preparing the next shift.",
)
filtered = filter_day_type(data, selected_day_type)
metrics = dashboard_metrics(filtered)

k1, k2, k3 = st.columns(3, gap="medium")
with k1:
    st.metric("Avg daily transactions", f"{metrics['avg_daily_transactions']:.1f}")
with k2:
    peak_hour = metrics["peak_hour"]
    st.metric("Busiest daytime hour", f"{peak_hour:02d}:00" if peak_hour is not None else "—")
with k3:
    st.metric("Most requested focus item", metrics["top_item"])

st.caption(
    f"Based on {metrics['transactions']:,} distinct transactions across "
    f"{metrics['observed_days']} recorded dates · "
    "Item popularity is the number of orders containing an item, not units sold."
)

st.subheader("When should the bakery prepare for demand?")
fig1 = plot_hourly(hourly_transaction_rates(filtered), metrics["peak_hour"])
st.pyplot(fig1, clear_figure=True, use_container_width=True)
plt.close(fig1)
st.caption(
    "Average orders per recorded day, by hour (08:00–17:59). The chart excludes "
    "late-night and very early transactions; overall daily KPI includes them. "
    "Dates without records are not assumed to be open days."
)

st.subheader("Which baked goods deserve preparation priority?")
fig2 = plot_product_windows(bakery_item_window_rates(filtered))
st.pyplot(fig2, clear_figure=True, use_container_width=True)
plt.close(fig2)
st.caption(
    "Distinct orders containing each selected baked good, averaged over recorded days. "
    "Morning and afternoon windows have different durations; comparisons are "
    "daily order incidence, not hourly demand or actual units sold."
)

with st.expander("Metric definitions and limitations"):
    st.markdown(
        """
- **Average daily transactions:** unique `Transaction` IDs / dates with at least one transaction.
- **Busiest daytime hour:** the clock hour with the highest transactions per recorded day in 08:00–17:59.
- **Most requested focus item:** the selected baked good contained in the most distinct transactions.
- **Focus baked goods:** Bread, Cake, Pastry, Medialuna, Cookies, Brownie, Muffin, and Scone.
- **Not measured:** revenue, waste, stock on hand, customer foot traffic, staff productivity, or exact production quantities.
- **Data caveats:** missing days may reflect closure or missing records; duplicate item rows may indicate multiple units; the dataset is a historical snapshot.
        """
    )

st.divider()
st.caption(
    "**Data period:** 2016-10-30 to 2017-04-09 (Kaggle historical snapshot) · "
    "**Production proposal:** refresh transactions nightly; manager reviews each morning "
    "and plans next week's preparation weekly. "
    "**Source:** [The Bread Basket on Kaggle]"
    "(https://www.kaggle.com/datasets/mittalvasu95/the-bread-basket)"
)
