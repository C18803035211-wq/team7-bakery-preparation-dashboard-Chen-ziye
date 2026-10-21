"""Transaction-level metrics for the Bakery Preparation Planning Dashboard.

One raw row is an item entry, not necessarily one sale or one order.
We treat repeated Transaction + Item pairs as a single item incidence when
studying product popularity; this does NOT estimate item quantities sold.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent / "data" / "bread_basket.csv"
REQUIRED_COLUMNS = {
    "Transaction", "Item", "date_time", "period_day", "weekday_weekend"
}
# Deliberate, non-exhaustive selection of recognizable bakery-preparation items.
# Coffee, tea, soup, sandwiches, merchandise, etc. are out of scope.
FOCUS_ITEMS = (
    "Bread", "Cake", "Pastry", "Medialuna", "Cookies", "Brownie",
    "Muffin", "Scone",
)
DISPLAY_HOURS = tuple(range(8, 18))  # 08:00 through 17:59
TIME_WINDOWS = ("Morning (08–11)", "Afternoon (12–16)")


def load_transactions(path: Path | str = DATA_FILE) -> pd.DataFrame:
    """Read and validate the original Kaggle snapshot; do NOT drop duplicates."""
    path = Path(path)
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame = frame.copy()
    frame["timestamp"] = pd.to_datetime(
        frame["date_time"], format="%d-%m-%Y %H:%M", errors="raise"
    )
    if frame[["Transaction", "Item", "timestamp"]].isna().any().any():
        raise ValueError("Unexpected null transaction ID, item or timestamp")
    frame["date"] = frame["timestamp"].dt.normalize()
    frame["hour"] = frame["timestamp"].dt.hour
    frame["day_type"] = frame["timestamp"].dt.dayofweek.map(
        lambda day: "Weekday" if day < 5 else "Weekend"
    )
    # The time segments are defined here, not inferred from shop opening hours.
    frame["preparation_window"] = "Outside primary preparation windows"
    frame.loc[frame["hour"].between(8, 11), "preparation_window"] = TIME_WINDOWS[0]
    frame.loc[frame["hour"].between(12, 16), "preparation_window"] = TIME_WINDOWS[1]
    inconsistent_orders = (frame.groupby("Transaction")["timestamp"].nunique() > 1).sum()
    if inconsistent_orders:
        raise ValueError(f"{inconsistent_orders} transaction IDs have multiple timestamps")
    return frame


def filter_day_type(frame: pd.DataFrame, day_type: str) -> pd.DataFrame:
    if day_type not in ("All days", "Weekday", "Weekend"):
        raise ValueError(f"Unknown day type: {day_type}")
    if day_type == "All days":
        return frame.copy()
    return frame.loc[frame["day_type"] == day_type].copy()


def order_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """One row per order, for transaction-count KPIs."""
    return frame.drop_duplicates(subset=["Transaction"]).copy()


def item_order_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """One row per transaction + product; NOT the number of pieces sold."""
    return frame.drop_duplicates(subset=["Transaction", "Item"]).copy()


def dashboard_metrics(frame: pd.DataFrame) -> dict:
    orders = order_rows(frame)
    observed_days = orders["date"].nunique()
    if observed_days == 0:
        return {"observed_days": 0, "transactions": 0,
                "avg_daily_transactions": 0.0, "peak_hour": None,
                "top_item": "No data"}
    hourly = hourly_transaction_rates(frame)
    peak = int(hourly.idxmax()) if hourly.max() > 0 else None
    item_rows = item_order_rows(frame)
    item_counts = item_rows.loc[item_rows["Item"].isin(FOCUS_ITEMS), "Item"].value_counts()
    return {
        "observed_days": int(observed_days),
        "transactions": int(len(orders)),
        "avg_daily_transactions": len(orders) / observed_days,
        "peak_hour": peak,
        "top_item": str(item_counts.index[0]) if not item_counts.empty else "No data",
    }


def hourly_transaction_rates(frame: pd.DataFrame) -> pd.Series:
    """Avg transactions per observed date for each displayed clock hour.

    Recorded dates are the denominator, even when an hour has no recorded
    transactions. This is a demand proxy, not verified footfall or open hours.
    """
    days = order_rows(frame)["date"].nunique()
    counts = order_rows(frame).groupby("hour").size().reindex(DISPLAY_HOURS, fill_value=0)
    rates = counts / days if days else counts.astype(float)
    rates.index.name = "Hour"
    rates.name = "Avg transactions / recorded day"
    return rates


def bakery_item_window_rates(frame: pd.DataFrame, top_n: int = 6) -> pd.DataFrame:
    """Long-form daily incidence rates of focus items by time window."""
    obs_days = order_rows(frame)["date"].nunique()
    item_orders = item_order_rows(frame)
    relevant = item_orders.loc[
        item_orders["Item"].isin(FOCUS_ITEMS)
        & item_orders["preparation_window"].isin(TIME_WINDOWS)
    ]
    counts = relevant.groupby(["Item", "preparation_window"]).size()
    pivot = counts.unstack(fill_value=0).reindex(columns=TIME_WINDOWS, fill_value=0)
    if pivot.empty:
        return pd.DataFrame(columns=list(TIME_WINDOWS), dtype=float)
    # Rank items by total number of recorded transactions containing that item.
    top_items = pivot.sum(axis=1).sort_values(ascending=False).head(top_n).index
    pivot = pivot.loc[top_items]
    return pivot.astype(float) / obs_days if obs_days else pivot.astype(float)


def daily_transactions(frame: pd.DataFrame) -> pd.DataFrame:
    """Transactions on each *observed* date. Gaps are unknown, not zeros."""
    return (
        order_rows(frame).groupby(["date", "day_type"]).size()
        .rename("transactions").reset_index().sort_values("date")
    )
