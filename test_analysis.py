"""Small audit tests to catch mistakes in order/item counting."""
import unittest
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bakery_analysis import (
    DATA_FILE, FOCUS_ITEMS, TIME_WINDOWS,
    load_transactions, order_rows, item_order_rows,
    filter_day_type, dashboard_metrics,
    bakery_item_window_rates, hourly_transaction_rates,
)


class BakeryAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_transactions(DATA_FILE)

    def test_source_counts(self):
        self.assertEqual(len(self.raw), 20507)
        self.assertEqual(len(order_rows(self.raw)), 9465)
        self.assertEqual(self.raw["Item"].nunique(), 94)

    def test_duplicate_item_rows_not_orders(self):
        # Same basket + item can appear several times; should count once as
        # an order containing the item, without claiming units purchased.
        raw_count = int((self.raw["Item"] == "Coffee").sum())
        incidence_count = int((item_order_rows(self.raw)["Item"] == "Coffee").sum())
        self.assertGreater(raw_count, incidence_count)
        self.assertEqual(incidence_count, 4528)

    def test_day_type_averages(self):
        wd = dashboard_metrics(filter_day_type(self.raw, "Weekday"))
        we = dashboard_metrics(filter_day_type(self.raw, "Weekend"))
        self.assertEqual((wd["transactions"], wd["observed_days"]), (6145, 113))
        self.assertEqual((we["transactions"], we["observed_days"]), (3320, 46))
        self.assertGreater(we["avg_daily_transactions"], wd["avg_daily_transactions"])

    def test_figures_inputs_and_hourly_denominator(self):
        m = dashboard_metrics(self.raw)
        self.assertEqual(m["peak_hour"], 11)
        h = hourly_transaction_rates(self.raw)
        self.assertAlmostEqual(h.loc[11], 1439 / 159)
        pivot = bakery_item_window_rates(self.raw)
        self.assertFalse(pivot.empty)
        self.assertTrue(set(pivot.columns) == set(TIME_WINDOWS))


if __name__ == "__main__":
    unittest.main()
