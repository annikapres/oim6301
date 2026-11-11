import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb
    import matplotlib.pyplot as plt
    import polars as pl

    return duckdb, pl, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Babson Bean Cafe Database

    The build cell recreates `database.duckdb` from the CSV files each time this notebook runs.
    """)
    return


@app.cell
def _(mo):
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables.

    One CREATE TABLE for each table in your ERD, with every primary key and foreign key declared, and with NOT NULL, CHECK, UNIQUE and DEFAULT where the scenario's rules call for them. Chapter D of the SQL handbook, §24, has the syntax


    Each table declares its primary and foreign keys. `CHECK`, `UNIQUE` and `DEFAULT` enforce the café's column-level rules; payment totals are checked by a query because they span tables. Every generated order has at least one line, because a foreign key cannot require an order to have a child row.
    """)
    return


@app.cell
def _(database, duckdb, mo):
    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                mobile_number VARCHAR NOT NULL UNIQUE,
                email VARCHAR UNIQUE,
                join_date DATE NOT NULL,
                points_balance INTEGER NOT NULL DEFAULT 0 CHECK (points_balance >= 0)
            );

            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                category VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
                price DECIMAL(10,2) NOT NULL CHECK (price >= cost),
                cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0),
                is_available BOOLEAN NOT NULL DEFAULT TRUE
            );

            CREATE TABLE options (
                option_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
                cost DECIMAL(10,2) NOT NULL CHECK (cost >= 0)
            );

            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                ordered_at TIMESTAMP NOT NULL,
                member_id INTEGER REFERENCES members(member_id),
                channel VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
            );

            CREATE TABLE order_lines (
                line_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                product_id INTEGER NOT NULL REFERENCES products(product_id),
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0)
            );

            CREATE TABLE line_options (
                line_id INTEGER NOT NULL REFERENCES order_lines(line_id),
                option_id INTEGER NOT NULL REFERENCES options(option_id),
                price_charged DECIMAL(10,2) NOT NULL CHECK (price_charged >= 0),
                PRIMARY KEY (line_id, option_id)
            );

            CREATE TABLE payments (
                payment_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                method VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
                amount DECIMAL(10,2) NOT NULL CHECK (amount > 0)
            );
        """)

        for _table in (
            "members",
            "products",
            "options",
            "orders",
            "order_lines",
            "line_options",
            "payments",
        ):
            _csv_path = (mo.notebook_dir() / "data" / f"{_table}.csv").as_posix()
            _csv_path = _csv_path.replace("'", "''")
            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv_auto('{_csv_path}')"
            )

        _con.execute("""
            CREATE VIEW weekly_category_revenue AS
            WITH line_sales AS (
                SELECT p.category, SUM(ol.quantity * ol.price_charged) AS revenue
                FROM orders AS o
                JOIN order_lines AS ol ON ol.order_id = o.order_id
                JOIN products AS p ON p.product_id = ol.product_id
                WHERE o.ordered_at >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY p.category
                UNION ALL
                SELECT p.category, SUM(ol.quantity * lo.price_charged) AS revenue
                FROM orders AS o
                JOIN order_lines AS ol ON ol.order_id = o.order_id
                JOIN products AS p ON p.product_id = ol.product_id
                JOIN line_options AS lo ON lo.line_id = ol.line_id
                WHERE o.ordered_at >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY p.category
            )
            SELECT category, SUM(revenue) AS revenue
            FROM line_sales
            GROUP BY category
        """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data.


    Ask your agent for a script, projects/db/make_data.py, that writes data for every table as CSV files in projects/db/data/, and load them. The data has to obey every rule, with one exception: for each question marked (checks a rule) on your list, break its rule on purpose in exactly two rows, and write down which two in this section. If your tables make the database refuse those rows, your design holds that rule with a constraint: say so here, and show the refusal in that question's answer instead. It has to cover the 12 months up to a date you choose, your as_of date, which Part B uses. You can start from this prompt. Replace each part in angle brackets, brackets included, with your own text:

    Here are the CREATE TABLE statements for my database: <your CREATE TABLE statements>.
    Write a Python script, projects/db/make_data.py, that writes one CSV file
    per table into projects/db/data/.
    - Follow every rule of my scenario: <your scenario's rules>.
    - Break these rules on purpose, each in exactly two rows, and print which rows:
      <the rules your checking questions are about>.
    - Make <your scenario's amounts of data>, covering the 12 months up to <your as_of date>.
    - Include on purpose some rows with nothing attached, such as <one from your scenario>.
    - Use a fixed random seed, so that the script writes the same files every time.

    Copy


    Your scenario says how much data it needs; for your own domain, at least 10 rows in each table that lists things the business keeps and 1,000 rows across the tables that record what happens. Include on purpose some rows with nothing attached, so that the questions about them have an answer. Read the data before you keep it, because an agent's first try usually breaks a rule nobody wrote down: a task assigned before somebody started, a sale of shares nobody held, two appointments at once, a price nobody would charge.



    Run `uv run python projects/db/make_data.py` to regenerate the seven CSV files with a fixed seed. The 12-month period is November 12, 2025 through November 11, 2026 (`as_of`). It contains 40 members, 20 products, 8 options, and 1,000 orders.

    The only deliberate rule breaks are the two payment-total exceptions in the checking question: order 1 has no payment, and order 2 is underpaid by $1.00. Every other row follows the declared rules. Some members never order, some orders have no member, some order lines have no options, and products/options are intentionally unsold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data.

    Read one of your CSV files with polars and chart one column whose shape you can judge, such as appointments by day of the week, orders by hour, or one asset's closing prices. Write one sentence on whether a real business would look like that, and if it would not, what you changed in make_data.py.


    The weekday-heavy order pattern is plausible for a campus cafe; `make_data.py` deliberately assigns about 86% of orders to weekdays.
    """)
    return


@app.cell
def _(mo, pl, plt):
    orders_preview = pl.read_csv(
        mo.notebook_dir() / "data" / "orders.csv", try_parse_dates=True
    )
    weekday_counts = (
        orders_preview.with_columns(
            pl.col("ordered_at").dt.weekday().alias("weekday_number")
        )
        .group_by("weekday_number")
        .agg(pl.len().alias("orders"))
        .sort("weekday_number")
        .with_columns(
            pl.col("weekday_number")
            .replace_strict(
                {
                    1: "Monday",
                    2: "Tuesday",
                    3: "Wednesday",
                    4: "Thursday",
                    5: "Friday",
                    6: "Saturday",
                    7: "Sunday",
                }
            )
            .alias("weekday")
        )
    )
    _figure, _axes = plt.subplots(figsize=(8, 4))
    _axes.bar(weekday_counts["weekday"].to_list(), weekday_counts["orders"].to_list())
    _axes.set_title("Orders by Day of Week")
    _axes.set_ylabel("Orders")
    _figure.tight_layout()
    _figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts.

    Every table with its number of rows.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'members' AS table_name, COUNT(*) AS row_count FROM members
        UNION ALL SELECT 'products', COUNT(*) FROM products
        UNION ALL SELECT 'options', COUNT(*) FROM options
        UNION ALL SELECT 'orders', COUNT(*) FROM orders
        UNION ALL SELECT 'order_lines', COUNT(*) FROM order_lines
        UNION ALL SELECT 'line_options', COUNT(*) FROM line_options
        UNION ALL SELECT 'payments', COUNT(*) FROM payments
        ORDER BY table_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses.

    Insert one row that breaks one of your rules, and show the message the database gives back. ask() only reads, so open a short write connection of its own for the insert, with duckdb.connect(database) as _con:, the way notebook 6 does, and put it inside try and except, so that the rest of the notebook still runs.

    A coffee that costs the shop $5.00 but is sold for $1.00: the `CHECK (price >= cost)` constraint on `products` holds the rule "a product's price is never below its cost", so the database refuses it.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute(
                "INSERT INTO products VALUES (9001, 'Priced Below Cost', 'coffee', 1.00, 5.00, true)"
            )
        refused = "accepted"
    except duckdb.ConstraintException as _error:
        refused = str(_error).splitlines()[0]
    refused
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew.

    Three queries whose answers you knew before you ran them, because you know what you asked your agent for, with the answer you expected written next to each.



    | Query | Expected answer |
    |---|---:|
    | `SELECT COUNT(*) FROM orders` | 1,000 |
    | `SELECT COUNT(*) FROM members` | 40 |
    | `SELECT COUNT(*) FROM options` | 8 |
    """)
    return


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS orders FROM orders")
    return


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS members FROM members")
    return


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS options FROM options")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View.

    One question the business would ask every week, saved with CREATE VIEW in the cell that builds the database, so that anybody can ask for it by name and always get the current rows. Notebook 6 covers views in section 5, after GROUP BY. At least one of your answers in Part B must use it. Chapter D of the SQL handbook, §28.

    A weekly question: how much revenue did each menu category bring in over the last seven days? The view is created during the rebuild and includes product lines and their options.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM weekly_category_revenue ORDER BY revenue DESC")
    return


if __name__ == "__main__":
    app.run()
