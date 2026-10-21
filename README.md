# 🥐 Bakery Preparation Planning Dashboard

> **Team:** Team 7  
> **Student / individual submission owner:** Chen ziye  
> **Status:** Educational prototype, not a live operational dashboard.

## Project overview

**Decision-maker:** One bakery store manager.

**Recurring decision:** When should the bakery prioritize preparation, and which baked goods should be ready before its busiest periods?

**Business setting:** The manager prepares the next day's bakery-product plan and reviews the following week's schedule. Preparing too early may create waste; preparing too late could contribute to unavailable items or missed purchases. Those impacts are plausible operational risks, **not outcomes measured in this dataset**.

**Decision statement:** *If the manager sees that transactions consistently cluster around a certain hour and that specific baked goods appear more frequently in morning versus afternoon orders, they will review preparation timing and prioritize those products before the relevant demand period.*

Our goal is **preparation priorities**, not exact production quantities, inventory optimization, or profit forecasting.

## Step 1 — Dataset and decision-maker

- **Dataset:** [The Bread Basket — Kaggle](https://www.kaggle.com/datasets/mittalvasu95/the-bread-basket)
- **File used:** `data/bread_basket.csv` (single CSV, ~0.98 MB)
- **Claimed origin:** The Kaggle description identifies an Edinburgh bakery's transactions. The independently verified provenance of individual entries is not supplied; this project treats them as a historical business-record dataset as described by its publisher, rather than asserting independent authenticity.
- **Actual range in the supplied CSV:** **2016-10-30 through 2017-04-09**, not current data.
- **Actual file shape:** **20,507 rows, 5 columns** — `Transaction`, `Item`, `date_time`, `period_day`, `weekday_weekend`.
- **What one row means:** One *item entry* belonging to a transaction, with a timestamp and two derived time descriptors. Several rows may share a transaction identifier. The data has **no explicit item quantity** field.
- **Source metadata note:** Kaggle description text may cite a different date notation or column count. The numbers and time range in this report come from the **CSV you uploaded and can reproduce**, not from assuming web metadata matches every exported version.

**Single target user:** Bakery Store Manager. This is not a dashboard for customers, a corporate CFO, or all employees.

## Step 2 — Why a dashboard, instead of a report?

**1. Who looks, how often?** The manager checks the dashboard each morning and revisits it once a week when preparing the following week's schedule. These are **proposed routines for a real operational deployment**, not observed behavior in the CSV.

**2. What decision?** Prioritize baked-goods preparation before recurring high-demand hours, using weekday/weekend comparisons and product-by-time breakdowns. Example: if pastry-containing orders are more frequent in mornings, the manager may plan pastry preparation earlier; if cake-containing orders are more frequent in afternoons, review cake availability ahead of that period.

**3. What happens without it?** In the hypothetical business workflow, the manager may rely on memory or manually calculate totals from POS exports. That costs administrative time and can hide differences between weekdays and weekends. The file does **not** measure this time cost or operational savings.

**4. Why a dashboard rather than a weekly email, report, or alert?** This decision recurs as new transaction records arrive. The manager needs to switch between weekday and weekend demand and compare *when* (hourly order volume) with *what* (priority baked goods). A weekly email or static report can summarize known patterns, but cannot as conveniently support follow-up comparisons for different day types. An alert could flag an unusual increase in orders, but it would not explain which hours or products deserve attention. Alerts would complement this dashboard rather than replace it. The dashboard earns its place through a focused, repeatable preparation-planning workflow.

## Step 3 — EDA findings and dashboard decisions

The reproducible notebook is [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb), using **Pandas and Matplotlib**.

### Data quality and metric definitions

| Check | Actual result / decision |
| --- | --- |
| Total item rows | **20,507** |
| Unique `Transaction` IDs | **9,465** |
| Unique item labels | **94** |
| Dates containing at least one transaction | **159** |
| File date range | **2016-10-30 to 2017-04-09** |
| Missing cells in the five raw columns | **0** |
| Exactly duplicated raw rows | **1,620** |
| Transaction IDs mapped to multiple timestamps | **0** |
| Calendar dates without any records inside the span | **2016-12-25, 2016-12-26, 2017-01-02** |

**Critical accounting choice:** `Transaction.nunique()` counts orders, while an item-incidence metric counts unique `(Transaction, Item)` pairs. We deliberately do **not** globally delete the 1,620 repeated item rows, because they *might* indicate multiple units in one order. Neither row totals nor deduplicated pairs reliably measure **units sold**, since explicit quantities are absent. This is why all charts refer to **orders containing an item**, not item units or revenue.

**Daily averages** are divided by the number of *recorded dates* in each day-type category. Days with no records are **unknown** (possibly closed/missing), not imputed as zero sales. The unusually sparse record on Jan 1, 2017 (one transaction at 01:21) should be treated cautiously, not silently removed.

### Initial evidence from the uploaded CSV

- **Weekday:** 6,145 orders across 113 recorded dates = **54.4 orders / recorded date**.
- **Weekend:** 3,320 orders across 46 recorded dates = **72.2 orders / recorded date** (**32.7%** higher than weekdays). This is descriptive, not proof that weekends cause higher sales.
- **Busiest daytime hour (by total distinct transactions):** **11:00–11:59**, with **1,439 transactions** in the entire historical snapshot.
- **Morning (08–11):** `Pastry` is present in **570** distinct orders; **Afternoon (12–16):** it is present in **233** orders.
- **Morning (08–11):** `Cake` is present in **259** distinct orders; **Afternoon (12–16):** it is present in **696** orders.

Morning (4 hours) and afternoon (5 hours) differ in duration; the second chart is normalized **per recorded date**, not per hour. The patterns suggest *which products to review for preparation* but do not quantify how much to bake.

### Why the three headline KPIs?

1. **Average daily transactions**: expected scale of a comparable recorded day; divided by observed dates to avoid confusing more observed weekdays with greater per-day demand.
2. **Busiest daytime hour**: quick answer to *when* preparation or counter readiness deserves attention. Derived from 08:00–17:59, rather than letting isolated late-night entries create a false peak.
3. **Most requested focus item**: a quick pointer toward *what* the manager should prioritize for a given day type, measured by the number of distinct orders containing the item.

### Why these two charts?

- **Chart 1 — Average hourly transactions:** helps explain the peak-hour KPI and when to prioritize preparation. It displays 08:00–17:59 and divides hourly transactions by all recorded dates in the selected day type.
- **Chart 2 — Baked goods by preparation window:** compares selected bakery items for morning versus afternoon, helping explain which product-category preparations deserve attention.

**Only one interactive filter:** `All days / Weekday / Weekend`, because that choice directly changes the manager's preparation plan. We intentionally do not add ten product or date sliders.

**Focus bakery items:** Bread, Cake, Pastry, Medialuna, Cookies, Brownie, Muffin, Scone. This is an **explicit hand-selected operational scope** based on clearly recognizable baked goods, *not* a claim to classify all 94 item names automatically. Coffee, Tea, Soup, Sandwich, and non-food merchandise are not baked-goods preparation priorities in this prototype.

### Two analyses deliberately excluded from the dashboard

1. **All 94 product labels ranked together:** overwhelms the manager, and coffee/drinks obscure the baking-specific decision. We instead show a small, explicit focus set.
2. **Raw monthly transaction totals:** the dataset begins partway through October 2016 and ends partway through April 2017, and the number of recorded days varies across months. Unadjusted monthly totals would therefore give a misleading impression of changes in demand. They also do not directly tell the manager what to prepare before a particular shift, so we prioritize hourly and product-by-time comparisons instead.

### What could mislead a viewer?

- Duplicate `(Transaction, Item)` rows can represent multiple units; interpreting them as multiple distinct orders inflates order prevalence. We count unique order–item pairs for the product chart.
- There is no sales price, cost, inventory, waste, or staffing data, so the dashboard cannot report revenue, waste reduction, shortage rates, or required production quantities.
- The dataset includes atypical overnight transactions and three unrecorded calendar dates. Main-hour charts omit overnight hours; missing days are not assumed to be open.
- The file covers a short historical period, not a full year and not today's demand. Holiday effects and seasonal trends may differ in the current store.
- Morning (08:00–11:59) and afternoon (12:00–16:59) preparation windows have different lengths. The product chart reports orders containing each item **per recorded date**, not per hour. These bars must not be interpreted as comparable hourly demand or staff productivity.

### Page order

**Top:** three KPIs (current situation), **middle:** two explanatory charts (when and what), **bottom:** small metric definitions, data limitations, source, and refresh notice. No unnecessary raw table: the manager makes shift-planning choices from the two focused breakdowns.

## Step 4 — Refresh frequency, review and action trigger

**Current class prototype:** The Kaggle CSV is a **frozen historical snapshot** covering 2016-10-30 to 2017-04-09. The app calculates descriptive historical KPIs and charts. It **does not** fetch live transactions, track current weeks, or send automatic alerts.

**Proposed real-business version** (assuming access to an authorized point-of-sale/POS data feed):

- **Data refresh:** nightly after closing, once the previous day's transactions are complete. More frequent refreshes would add complexity without changing the daily/weekly preparation decision.
- **Manager review:** each morning before the day's preparation, plus a weekly review when planning the next week's work.
- **Metric monitored over time:** average number of transactions between **11:00 and 11:59 per comparable open day**, separated by weekday versus weekend. Unlike the class prototype's recorded-date denominator, a real POS system should explicitly establish which days the bakery was open.
- **Illustrative action threshold:** if this peak-hour average is **more than 20% above the preceding four-week comparable baseline for two consecutive complete weeks**, the manager investigates. This **20% rule is a proposed trial policy**, not a statistical result derived or validated from this CSV. A real bakery would calibrate it against its own recent operating data and typical fluctuations.
- **Action after the threshold:** review the time-of-day pattern and which baked goods are commonly included in those orders; talk with the bakery team and adjust preparation priorities or timing for the following schedule. An alert can prompt this review, while the dashboard supplies the context for the decision.
- **Cost of stale data:** a one-day delay would generally have limited impact on a weekly plan, but a week of missing transactions could hide a sustained shift in customer demand. The dataset has no inventory, waste, or cost fields, so lost sales and waste costs cannot be quantified.
- **Why not real-time:** these preparation decisions are made before a shift or during weekly planning, not on a second-by-second basis.

**Data-period and refresh note in the app:** clearly identifies the 2016–2017 historical snapshot and the intended nightly refresh / daily review schedule for a possible production version.

## Step 5 — Run, deploy and submit

### Run locally using uv

Install Python package manager [uv](https://docs.astral.sh/uv/getting-started/installation/) and, from this repository root, run:

```bash
uv sync
uv run streamlit run app.py
```

The `.python-version` file requests **Python 3.14** per the course instructions. If uv needs to download that Python version, let it complete. App appears at a local address such as `http://localhost:8501`.

To run data-quality tests:

```bash
uv run python -m unittest discover -s tests -v
```

The EDA notebook is a supplementary analytical artifact; all app dependencies are declared in `pyproject.toml` and `requirements.txt`. On Community Cloud, `requirements.txt` is used when no `uv.lock` is committed.

### Deploy

1. **Personalization check:** This README identifies **Team 7** and **Chen ziye**. Make sure `TEAM_NAME` near the top of `app.py` also reads `Team 7` before deployment, so the web page matches the report. Each student must understand and be able to explain their own analysis.
2. Upload this project's **contents** (including `data/bread_basket.csv`) to **your own public GitHub repository**. Do not upload the zip alone.
3. Open [Streamlit Community Cloud](https://share.streamlit.io/) → **Create app** → **Yup, I have an app**.
4. Choose **your** repository, branch `main`, main file `app.py`.
5. Under **Advanced settings**, select **Python 3.14** (your instructor's explicit request), then **Save → Deploy**.
6. Test that charts change when you select `Weekday` versus `Weekend` and verify historical-data captions.
7. In Canvas, **each student submits individually:** (1) deployed app URL and (2) their **own** GitHub repository URL with an individual README.

If the Python 3.14 deployment reports a dependency error, first read Community Cloud's build logs and adjust the package constraints to published compatible versions; do not silently use a different Python version from the instructor's requirement.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface, KPIs and two decision charts |
| `bakery_analysis.py` | Reusable, auditable KPI and filtering calculations |
| `data/bread_basket.csv` | Uploaded historical CSV |
| `notebooks/01_eda.ipynb` | EDA using Pandas and Matplotlib |
| `tests/test_analysis.py` | Validation tests for data semantics and calculations |
| `requirements.txt` / `pyproject.toml` | Dependencies and uv configuration |
| `.python-version` | Instructor-required Python 3.14 |
| `START_HERE_中文.md` | Chinese click-by-click deployment guide |

### References

- Dataset: https://www.kaggle.com/datasets/mittalvasu95/the-bread-basket
- uv guide: https://docs.astral.sh/uv/guides/projects/
- Streamlit Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
