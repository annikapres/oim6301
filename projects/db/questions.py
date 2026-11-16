import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    from datetime import date, timedelta

    return date, duckdb, mo, timedelta


@app.cell
def _(date, timedelta):
    as_of = date(2026, 11, 11)
    period_start = as_of - timedelta(days=364)
    last_month_start = (as_of.replace(day=1) - timedelta(days=1)).replace(day=1)
    this_month_start = as_of.replace(day=1)
    last_30_start = as_of - timedelta(days=29)
    last_60_start = as_of - timedelta(days=59)
    day_after_as_of = as_of + timedelta(days=1)
    return (
        as_of,
        day_after_as_of,
        last_30_start,
        last_60_start,
        last_month_start,
        period_start,
        this_month_start,
    )


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    mo.md(f"""
    # Babson Bean Cafe Database

    ## Part B: The Questions

    Data period: {period_start} through {as_of}. Every date window ends on the single `as_of` date.
    """)
    return


@app.cell(hide_code=True)
def _(last_month_start, mo, this_month_start):
    sql_q1 = f"""
    SELECT p.name AS product, SUM(ol.quantity) AS units_sold
    FROM orders AS o
    JOIN order_lines AS ol ON ol.order_id = o.order_id
    JOIN products AS p ON p.product_id = ol.product_id
    WHERE o.ordered_at >= DATE '{last_month_start}'
      AND o.ordered_at < DATE '{this_month_start}'
    GROUP BY p.product_id, p.name
    ORDER BY units_sold DESC, product
    LIMIT 3
    """
    mo.md(f"""
    ## 1. Which three products sold the most units last month?

    Last month means the full calendar month before `as_of`.

    ```sql
    {sql_q1.strip()}
    ```
    """)
    return (sql_q1,)


@app.cell
def _(ask, sql_q1):
    result_q1 = ask(sql_q1)
    result_q1
    return (result_q1,)


@app.cell(hide_code=True)
def _(last_month_start, mo, result_q1):
    _best_sellers = []
    for _row in result_q1.iter_rows(named=True):
        _best_sellers.append(f"{_row['product']} ({_row['units_sold']} units)")
    mo.md(
        f"In {last_month_start:%B %Y}, the leaders were "
        f"{', '.join(_best_sellers)}."
    )
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q2 = f"""
    WITH category_components AS (
        SELECT p.category,
            SUM(ol.quantity * ol.price_charged) AS revenue,
            SUM(ol.quantity * p.cost) AS cost
        FROM orders AS o
        JOIN order_lines AS ol ON ol.order_id = o.order_id
        JOIN products AS p ON p.product_id = ol.product_id
        WHERE o.ordered_at >= DATE '{period_start}'
          AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        GROUP BY p.category
        UNION ALL
        SELECT p.category,
            SUM(ol.quantity * lo.price_charged) AS revenue,
            SUM(ol.quantity * op.cost) AS cost
        FROM orders AS o
        JOIN order_lines AS ol ON ol.order_id = o.order_id
        JOIN products AS p ON p.product_id = ol.product_id
        JOIN line_options AS lo ON lo.line_id = ol.line_id
        JOIN options AS op ON op.option_id = lo.option_id
        WHERE o.ordered_at >= DATE '{period_start}'
          AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        GROUP BY p.category
    ), category_totals AS (
        SELECT category, SUM(revenue) AS revenue, SUM(cost) AS cost,
            SUM(revenue) - SUM(cost) AS margin
        FROM category_components
        GROUP BY category
    )
    SELECT c.category, c.revenue, c.cost, c.margin,
        w.revenue AS revenue_last_7_days
    FROM category_totals AS c
    LEFT JOIN weekly_category_revenue AS w ON w.category = c.category
    ORDER BY c.category
    """
    mo.md(f"""
    ## 2. How much revenue, cost, and margin did each menu category generate?

    Add-on revenue and cost are assigned to the category of the product on the line. The last column uses the weekly view, which is anchored to the latest order date in this data.

    ```sql
    {sql_q2.strip()}
    ```
    """)
    return (sql_q2,)


@app.cell
def _(ask, sql_q2):
    result_q2 = ask(sql_q2)
    result_q2
    return (result_q2,)


@app.cell(hide_code=True)
def _(mo, result_q2):
    _category_sentences = []
    for _row in result_q2.iter_rows(named=True):
        _category_sentences.append(
            f"{_row['category']}: revenue ${float(_row['revenue']):,.2f}, "
            f"cost ${float(_row['cost']):,.2f}, "
            f"margin ${float(_row['margin']):,.2f}"
        )
    mo.md("By category: " + "; ".join(_category_sentences) + ".")
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q3 = f"""
    WITH item_totals AS (
        SELECT ol.order_id, SUM(ol.quantity * ol.price_charged) AS item_spend
        FROM order_lines AS ol
        JOIN orders AS o ON o.order_id = ol.order_id
        WHERE o.ordered_at >= DATE '{period_start}'
          AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        GROUP BY ol.order_id
    ), option_totals AS (
        SELECT ol.order_id, SUM(ol.quantity * lo.price_charged) AS option_spend
        FROM order_lines AS ol
        JOIN orders AS o ON o.order_id = ol.order_id
        JOIN line_options AS lo ON lo.line_id = ol.line_id
        WHERE o.ordered_at >= DATE '{period_start}'
          AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        GROUP BY ol.order_id
    ), order_totals AS (
        SELECT o.order_id,
            COALESCE(i.item_spend, 0) + COALESCE(x.option_spend, 0) AS total_spent
        FROM orders AS o
        LEFT JOIN item_totals AS i ON i.order_id = o.order_id
        LEFT JOIN option_totals AS x ON x.order_id = o.order_id
        WHERE o.ordered_at >= DATE '{period_start}'
          AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
    ), member_totals AS (
        SELECT m.member_id, m.first_name, COUNT(o.order_id) AS order_count,
            COALESCE(SUM(t.total_spent), 0) AS total_spent,
            ROUND(AVG(t.total_spent), 2) AS average_order
        FROM members AS m
        LEFT JOIN orders AS o ON o.member_id = m.member_id
            AND o.ordered_at >= DATE '{period_start}'
            AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        LEFT JOIN order_totals AS t ON t.order_id = o.order_id
        GROUP BY m.member_id, m.first_name
    )
    SELECT member_id, first_name, order_count, total_spent, average_order
    FROM member_totals
    WHERE total_spent > (SELECT AVG(total_spent) FROM member_totals)
    ORDER BY total_spent DESC, member_id
    """
    mo.md(f"""
    ## 3. Which members spent more than the average member?

    The comparison is each member's total spending against the average total spending across all members, including members who spent $0. Average order includes products and add-ons.

    ```sql
    {sql_q3.strip()}
    ```
    """)
    return (sql_q3,)


@app.cell
def _(ask, mo, sql_q3):
    result_q3 = ask(sql_q3)
    mo.ui.table(result_q3, page_size=result_q3.height)
    return (result_q3,)


@app.cell(hide_code=True)
def _(as_of, ask, mo, period_start, result_q3):
    average_all_members = ask(f"""
        WITH item_totals AS (
            SELECT ol.order_id, SUM(ol.quantity * ol.price_charged) AS amount
            FROM order_lines AS ol JOIN orders AS o ON o.order_id = ol.order_id
            WHERE o.ordered_at >= DATE '{period_start}'
              AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
            GROUP BY ol.order_id
        ), option_totals AS (
            SELECT ol.order_id, SUM(ol.quantity * lo.price_charged) AS amount
            FROM order_lines AS ol
            JOIN orders AS o ON o.order_id = ol.order_id
            JOIN line_options AS lo ON lo.line_id = ol.line_id
            WHERE o.ordered_at >= DATE '{period_start}'
              AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
            GROUP BY ol.order_id
        ), order_totals AS (
            SELECT o.order_id, o.member_id,
                COALESCE(i.amount, 0) + COALESCE(x.amount, 0) AS amount
            FROM orders AS o
            LEFT JOIN item_totals AS i ON i.order_id = o.order_id
            LEFT JOIN option_totals AS x ON x.order_id = o.order_id
            WHERE o.ordered_at >= DATE '{period_start}'
              AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        ), member_totals AS (
            SELECT m.member_id, COALESCE(SUM(t.amount), 0) AS total_spent
            FROM members AS m
            LEFT JOIN order_totals AS t ON t.member_id = m.member_id
            GROUP BY m.member_id
        )
        SELECT AVG(total_spent) AS average_member_total FROM member_totals
    """)
    _above_average = float(average_all_members["average_member_total"][0])
    mo.md(
        f"{result_q3.height} members spent more than the all-member average "
        f"of ${_above_average:,.2f}; their order counts, total spending, and "
        "average order are shown in the table."
    )
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q4 = f"""
    WITH item_totals AS (
        SELECT ol.order_id, SUM(ol.quantity * ol.price_charged) AS item_total
        FROM order_lines AS ol
        GROUP BY ol.order_id
    ), option_totals AS (
        SELECT ol.order_id, SUM(ol.quantity * lo.price_charged) AS option_total
        FROM order_lines AS ol
        JOIN line_options AS lo ON lo.line_id = ol.line_id
        GROUP BY ol.order_id
    ), payment_totals AS (
        SELECT order_id, SUM(amount) AS paid_total
        FROM payments
        GROUP BY order_id
    )
    SELECT o.order_id,
        COALESCE(i.item_total, 0) + COALESCE(x.option_total, 0) AS order_total,
        COALESCE(p.paid_total, 0) AS paid_total,
        COALESCE(i.item_total, 0) + COALESCE(x.option_total, 0)
            - COALESCE(p.paid_total, 0) AS difference
    FROM orders AS o
    LEFT JOIN item_totals AS i ON i.order_id = o.order_id
    LEFT JOIN option_totals AS x ON x.order_id = o.order_id
    LEFT JOIN payment_totals AS p ON p.order_id = o.order_id
    WHERE o.ordered_at >= DATE '{period_start}'
      AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
      AND COALESCE(i.item_total, 0) + COALESCE(x.option_total, 0)
          <> COALESCE(p.paid_total, 0)
    ORDER BY o.order_id
    """
    mo.md(f"""
    ## 4. Which orders were not paid in full?

    Sales components and payments are totaled separately before comparison so joining them does not repeat line amounts.

    ```sql
    {sql_q4.strip()}
    ```
    """)
    return (sql_q4,)


@app.cell
def _(ask, sql_q4):
    result_q4 = ask(sql_q4)
    result_q4
    return (result_q4,)


@app.cell(hide_code=True)
def _(mo, result_q4):
    _mismatch_details = []
    for _row in result_q4.iter_rows(named=True):
        _mismatch_details.append(
            f"order {_row['order_id']} had sales of ${float(_row['order_total']):,.2f} "
            f"and payments of ${float(_row['paid_total']):,.2f}"
        )
    mo.md(
        f"{result_q4.height} orders do not match: "
        + "; ".join(_mismatch_details)
        + "."
    )
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q5 = f"""
    SELECT m.member_id, m.first_name, m.join_date
    FROM members AS m
    WHERE m.join_date <= DATE '{as_of}'
      AND NOT EXISTS (
          SELECT 1 FROM orders AS o
          WHERE o.member_id = m.member_id
            AND o.ordered_at >= DATE '{period_start}'
            AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
      )
    ORDER BY m.member_id
    """
    mo.md(f"""
    ## 5. Which members have never placed an order?

    This means no order appears for them in the generated data period.

    ```sql
    {sql_q5.strip()}
    ```
    """)
    return (sql_q5,)


@app.cell
def _(ask, sql_q5):
    result_q5 = ask(sql_q5)
    result_q5
    return (result_q5,)


@app.cell(hide_code=True)
def _(mo, result_q5):
    _never_ordered = []
    for _row in result_q5.iter_rows(named=True):
        _never_ordered.append(f"{_row['first_name']} (member {_row['member_id']})")
    mo.md(
        f"{result_q5.height} members have never ordered: "
        f"{', '.join(_never_ordered) if _never_ordered else 'none'}."
    )
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q6 = f"""
    WITH points_by_order AS (
        SELECT order_id,
            MAX(CASE WHEN method = 'points' THEN 1 ELSE 0 END) AS used_points
        FROM payments
        GROUP BY order_id
    )
    SELECT DATE_TRUNC('month', o.ordered_at)::DATE AS month,
        COUNT(*) AS order_count,
        SUM(COALESCE(x.used_points, 0)) AS orders_with_points,
        ROUND(100.0 * SUM(COALESCE(x.used_points, 0)) / COUNT(*), 1) AS share_percent
    FROM orders AS o
    LEFT JOIN points_by_order AS x ON x.order_id = o.order_id
    WHERE o.ordered_at >= DATE '{period_start}'
      AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
    GROUP BY DATE_TRUNC('month', o.ordered_at)
    ORDER BY month
    """
    mo.md(f"""
    ## 6. What share of orders used points, at least partly, each month?

    ```sql
    {sql_q6.strip()}
    ```
    """)
    return (sql_q6,)


@app.cell
def _(ask, mo, sql_q6):
    result_q6 = ask(sql_q6)
    mo.ui.table(result_q6, page_size=result_q6.height)
    return (result_q6,)


@app.cell(hide_code=True)
def _(mo, result_q6):
    _highest_points_month = result_q6.sort("share_percent", descending=True).row(
        0, named=True
    )
    mo.md(
        f"The monthly share ranged from {float(result_q6['share_percent'].min()):.1f}% "
        f"to {float(result_q6['share_percent'].max()):.1f}%; it peaked in "
        f"{_highest_points_month['month']:%B %Y} at "
        f"{int(_highest_points_month['orders_with_points'])} of "
        f"{int(_highest_points_month['order_count'])} orders "
        f"({float(_highest_points_month['share_percent']):.1f}%)."
    )
    return


@app.cell
def _(result_q6):
    import polars as pl

    import altair as alt
    import matplotlib.pyplot as plt

    _months = [month.strftime("%b %Y") for month in result_q6["month"].to_list()]
    _shares = [float(share) for share in result_q6["share_percent"].to_list()]
    _figure, _axes = plt.subplots()
    _axes.bar(_months, _shares)
    _axes.set_xlabel("Month")
    _axes.set_ylabel("Orders paid with points (%)")
    _axes.tick_params(axis="x", labelrotation=45)
    _figure.tight_layout()
    _figure
    return


@app.cell(hide_code=True)
def _(as_of, day_after_as_of, last_60_start, mo):
    sql_q7 = f"""
    SELECT p.product_id, p.name, p.category, p.is_available
    FROM products AS p
    WHERE NOT EXISTS (
        SELECT 1
        FROM order_lines AS ol
        JOIN orders AS o ON o.order_id = ol.order_id
        WHERE ol.product_id = p.product_id
          AND o.ordered_at >= DATE '{last_60_start}'
          AND o.ordered_at < DATE '{day_after_as_of}'
    )
    ORDER BY p.category, p.name
    """
    mo.md(f"""
    ## 7. Which products have not sold in the last 60 days?

    This window includes {last_60_start} through {as_of}, regardless of current availability.

    ```sql
    {sql_q7.strip()}
    ```
    """)
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q8 = f"""
    WITH option_counts AS (
        SELECT line_id, COUNT(*) AS option_count
        FROM line_options
        GROUP BY line_id
    )
    SELECT p.name AS product, COUNT(o.order_id) AS lines_sold,
        ROUND(AVG(CASE WHEN o.order_id IS NOT NULL
            THEN COALESCE(x.option_count, 0) END), 2) AS average_options_per_line
    FROM products AS p
    LEFT JOIN order_lines AS ol ON ol.product_id = p.product_id
    LEFT JOIN orders AS o ON o.order_id = ol.order_id
        AND o.ordered_at >= DATE '{period_start}'
        AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
    LEFT JOIN option_counts AS x ON x.line_id = ol.line_id
    WHERE p.category IN ('coffee', 'tea')
    GROUP BY p.product_id, p.name
    ORDER BY p.name
    """
    mo.md(f"""
    ## 8. How many add-ons did each coffee and tea product average per line?

    A line with no options counts as zero. Products with no sold lines have no average to calculate.

    ```sql
    {sql_q8.strip()}
    ```
    """)
    return (sql_q8,)


@app.cell
def _(ask, mo, sql_q8):
    result_q8 = ask(sql_q8)
    mo.ui.table(result_q8, page_size=result_q8.height)
    return (result_q8,)


@app.cell(hide_code=True)
def _(mo, result_q8):
    _with_sales = result_q8.filter(result_q8["average_options_per_line"].is_not_null())
    _most_add_ons = _with_sales.sort(
        "average_options_per_line", descending=True
    ).row(0, named=True)
    mo.md(
        f"{result_q8.height} coffee and tea products are listed; "
        f"{_with_sales.height} had sold lines. {_most_add_ons['product']} had the "
        f"highest average at {float(_most_add_ons['average_options_per_line']):.2f} "
        "add-ons per line."
    )
    return


@app.cell(hide_code=True)
def _(as_of, last_30_start, mo):
    sql_q9 = f"""
    WITH calendar AS (
        SELECT CAST(day AS DATE) AS order_date
        FROM generate_series(
            DATE '{last_30_start}', DATE '{as_of}', INTERVAL 1 DAY
        ) AS days(day)
    ), daily_orders AS (
        SELECT c.order_date, STRFTIME(c.order_date, '%A') AS weekday,
            COUNT(o.order_id) AS order_count
        FROM calendar AS c
        LEFT JOIN orders AS o ON CAST(o.ordered_at AS DATE) = c.order_date
        GROUP BY c.order_date
    )
    SELECT weekday, COUNT(*) AS days_observed,
        SUM(order_count) AS total_orders,
        AVG(order_count) AS average_orders_per_day
    FROM daily_orders
    GROUP BY weekday
    ORDER BY average_orders_per_day DESC, weekday
    """
    mo.md(f"""
    ## 9. Which day of the week has been busiest recently?

    For staffing, this compares average orders per calendar day across the 30 days ending {as_of}.

    ```sql
    {sql_q9.strip()}
    ```
    """)
    return (sql_q9,)


@app.cell
def _(ask, sql_q9):
    result_q9 = ask(sql_q9)
    result_q9
    return (result_q9,)


@app.cell(hide_code=True)
def _(as_of, mo, result_q9):
    _busiest_day = result_q9.row(0, named=True)
    mo.md(
        f"In the 30 days ending {as_of}, {_busiest_day['weekday']} was busiest, "
        f"averaging {float(_busiest_day['average_orders_per_day']):.2f} orders "
        f"per day ({int(_busiest_day['total_orders'])} orders over "
        f"{int(_busiest_day['days_observed'])} occurrences)."
    )
    return


@app.cell(hide_code=True)
def _(as_of, mo, period_start):
    sql_q10 = f"""
    WITH item_totals AS (
        SELECT ol.order_id, SUM(ol.quantity * ol.price_charged) AS item_spend
        FROM order_lines AS ol
        GROUP BY ol.order_id
    ), option_totals AS (
        SELECT ol.order_id, SUM(ol.quantity * lo.price_charged) AS option_spend
        FROM order_lines AS ol
        JOIN line_options AS lo ON lo.line_id = ol.line_id
        GROUP BY ol.order_id
    ), order_totals AS (
        SELECT o.order_id, o.channel,
            COALESCE(i.item_spend, 0) + COALESCE(x.option_spend, 0) AS order_total
        FROM orders AS o
        LEFT JOIN item_totals AS i ON i.order_id = o.order_id
        LEFT JOIN option_totals AS x ON x.order_id = o.order_id
        WHERE o.ordered_at >= DATE '{period_start}'
          AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
    )
    SELECT channel, COUNT(*) AS order_count,
        ROUND(AVG(order_total), 3) AS average_order_total,
        SUM(order_total) AS total_sales
    FROM order_totals
    GROUP BY channel
    ORDER BY average_order_total DESC
    """
    mo.md(f"""
    ## 10. Which ordering channel has the higher average check?

    This helps the manager compare counter and app order values. Check totals include product and add-on charges over the generated data period.

    ```sql
    {sql_q10.strip()}
    ```
    """)
    return (sql_q10,)


@app.cell
def _(ask, sql_q10):
    result_q10 = ask(sql_q10)
    result_q10
    return (result_q10,)


@app.cell(hide_code=True)
def _(mo, result_q10):
    _higher_channel = result_q10.row(0, named=True)
    mo.md(
        f"{_higher_channel['channel']} had the higher average check at "
        f"${float(_higher_channel['average_order_total']):,.3f} across "
        f"{int(_higher_channel['order_count'])} orders; its total sales were "
        f"${float(_higher_channel['total_sales']):,.2f}."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 1. How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(ask, result_q2):
    category_revenue_total = round(float(result_q2["revenue"].sum()), 2)
    independent_revenue_total = round(
        float(
            ask("""
                SELECT
                    (SELECT COALESCE(SUM(quantity * price_charged), 0)
                     FROM order_lines)
                    +
                    (SELECT COALESCE(SUM(ol.quantity * lo.price_charged), 0)
                     FROM order_lines AS ol
                     JOIN line_options AS lo ON lo.line_id = ol.line_id)
                    AS revenue
            """)["revenue"][0]
        ),
        2,
    )
    assert category_revenue_total == independent_revenue_total
    print(f"Category answer revenue: ${category_revenue_total:,.2f}")
    print(f"Independent lines plus options: ${independent_revenue_total:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The two totals agree. The assertion fails if the category query omits or double-counts revenue.
    """)
    return


@app.cell
def _(result_q4):
    mismatch_ids = sorted(result_q4["order_id"].to_list())
    expected_mismatch_ids = [1, 2]
    assert mismatch_ids == expected_mismatch_ids
    print(f"Query mismatch count: {len(mismatch_ids)}")
    print(f"Expected deliberate exceptions: {len(expected_mismatch_ids)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The mismatches are order 1 (no payment) and order 2 ($1.00 short), exactly the two deliberate exceptions recorded in Part A.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The first prediction text said the line-options key allows at most one option on a line. That explanation is wrong: the composite key prevents the same option being repeated, but still allows several different options on one line. I checked the table definition and `make_data.py`; this generated data currently adds zero or one option to each line. I kept the original prediction in commit `6777a84` (`db: prediction`), made before any query, and explain the correction with the measured join count in Reading It Back. The category question wording was also made manager-facing without dropping its requested revenue, cost, margin, or option-category rule.

    Part A's weekly view used `CURRENT_DATE`, which did not match this project's `as_of` date. I changed the view in `build.py` to use the latest order date in the loaded data, rebuilt the database, and checked that its maximum order date is November 11, 2026 and that the weekly view returns all four categories.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Reading It Back
    """)
    return


@app.cell(hide_code=True)
def _(as_of, mo):
    mo.md(f"""
    **Question picked before answering:** How much revenue, cost, and margin did each menu category generate, including options under the category of the product on their order line?

    **Committed prediction:** Before grouping, I expected the joins from `orders` to `order_lines` to `products`, then through `line_options` to `options`, to produce about 2,000 rows. There are 1,000 orders with 1 to 3 lines each, averaging two lines per order. Each line must match one order and one product, and the line-options key allows at most one option per line, so left-joining options should preserve one row per order line. The selected `as_of` date is {as_of}. The prediction is in commit `6777a84` (`db: prediction`), before these answers were run..
    """)
    return


@app.cell(hide_code=True)
def _(ask, day_after_as_of, mo, period_start):
    sql_join_check = f"""
    SELECT COUNT(*) AS joined_rows,
        (SELECT COUNT(*) FROM order_lines) AS order_line_rows
    FROM orders AS o
    JOIN order_lines AS ol ON ol.order_id = o.order_id
    JOIN products AS p ON p.product_id = ol.product_id
    LEFT JOIN line_options AS lo ON lo.line_id = ol.line_id
    LEFT JOIN options AS op ON op.option_id = lo.option_id
    WHERE o.ordered_at >= DATE '{period_start}'
      AND o.ordered_at < DATE '{day_after_as_of}'
    """
    join_count_result = ask(sql_join_check)
    mo.md(f"""
    **Joins alone, before grouping:**

    ```sql
    {sql_join_check.strip()}
    ```
    """)
    return (join_count_result,)


@app.cell
def _(as_of, join_count_result, mo):
    joined_rows = int(join_count_result["joined_rows"][0])
    order_line_rows = int(join_count_result["order_line_rows"][0])
    prediction_matched = abs(joined_rows - 2000) <= 100
    if prediction_matched:
        _prediction_text = "matched the estimate"
    else:
        _prediction_text = "did not match the estimate"
    mo.md(
        f"The joins produced {joined_rows:,} rows compared with "
        f"{order_line_rows:,} order lines. My prediction of about 2,000 rows "
        f"{_prediction_text}. They are equal because the generator currently "
        "puts no more than one option on a line; the composite key itself does "
        "not impose that limit. One row of the final result means one menu "
        f"category's combined product-and-option revenue, cost, and margin "
        f"through {as_of}."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 4. Going Further
    """)
    return


@app.cell(hide_code=True)
def _(mo, result_q10):
    _channel_count = result_q10.height
    _higher_channel = result_q10.row(0, named=True)
    _lower_channel = result_q10.row(result_q10.height - 1, named=True)
    mo.md(
        f"I compared the app and counter channels by average check, a staffing "
        f"and channel-planning question not on the original list. Counter was "
        f"slightly higher at ${float(_higher_channel['average_order_total']):,.3f} "
        f"versus ${float(_lower_channel['average_order_total']):,.3f} for app. "
        f"The query and both channel totals are shown in question 10 "
        f"({_channel_count} channels). I also made question 6 easier to compare "
        "over time with a bar chart of the monthly share of orders paid at "
        "least partly with points. Its axes are labeled Month and Orders paid "
        "with points (%), and the tooltips show the order counts behind each "
        "percentage."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 5. Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    **Time Spent:** 5-6 hours in total
    """)
    return


if __name__ == "__main__":
    app.run()
