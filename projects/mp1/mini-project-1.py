# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A Reorder Simulation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Many restaurant companies would use this to reorder food items for their inventory when stock levels run low, ensuring they never run out of essential ingredients, and so that it also doesn't go bad. This automated reordering system helps maintain optimal stock levels, reduces manual tracking efforts, and minimizes the risk of running out of critical ingredients during peak business hours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I would solve these steps first by looking at daily demand : take the starting stock amount and start subtracting the daily demand. Keep in mind that it takes 3 days to deliver the 100 cartons, so have to keep the amount in stock above 40-60 before ordering the next shipment, since they they could go through 8-20 in a day. Then simulate day by day using a loop, tracking the current stock level, pending orders, and their arrival dates.

    Loop would carry the leftovers of the day before into the next as the current stock point and then subtract that day's demand to get the new stock level. When the running stock gets close to the reorder threshold (around 40-60 cartons), trigger a new order of 100 cartons, but remember it won't arrive for 3 days, so the stock will keep depleting during that lead time before the new shipment lands. Orders that have been placed but not delivered are tracked until their arrival day.

    I would check this in section 6 by making sure the total number of units sold plus the total number of units lost equals the total demand over the 30 days. The two numbers that should agree are total demand = total sold + total lost
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.
    return


@app.cell
def _():
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3
    reorder_points = [20, 30, 40, 50]
    daily_demand = [12, 15, 9, 14, 18, 11, 10, 16, 13, 17, 8, 12, 20, 14, 11,
                    9, 15, 13, 16, 12, 10, 14, 19, 11, 13, 15, 9, 12, 17, 14]
    return (
        daily_demand,
        lead_time_days,
        order_quantity,
        reorder_points,
        starting_stock,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell(hide_code=True)
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    reorder_point = 40
    stock = starting_stock
    order_due_day = -1  # -1 means "no order is currently on its way"

    starting_list = []
    arrived_list = []
    demand_list = []
    sold_list = []
    lost_list = []
    ending_list = []
    ordered_list = []

    for i in range(len(daily_demand)):
        day_start = stock
        arrived = 0

        if order_due_day == i:
            stock = stock + order_quantity
            arrived = order_quantity
            order_due_day = -1

        demand = daily_demand[i]
        if stock >= demand:
            sold = demand
            lost = 0
        else:
            sold = stock
            lost = demand - sold

        stock = stock - sold
        ordered = 0

        if stock <= reorder_point and order_due_day == -1:
            order_due_day = i + lead_time_days
            ordered = order_quantity

        starting_list.append(day_start)
        arrived_list.append(arrived)
        demand_list.append(demand)
        sold_list.append(sold)
        lost_list.append(lost)
        ending_list.append(stock)
        ordered_list.append(ordered)
    for i in range(len(daily_demand)):
        print(
            f"Day {i+1}: start={starting_list[i]}, arrived={arrived_list[i]}, "
            f"demand={demand_list[i]}, sold={sold_list[i]}, lost={lost_list[i]}, "
            f"end={ending_list[i]}, ordered={ordered_list[i]}"
        )
    return (
        arrived_list,
        demand_list,
        ending_list,
        lost_list,
        ordered_list,
        sold_list,
        starting_list,
    )


@app.cell
def _(
    arrived_list,
    daily_demand,
    demand_list,
    ending_list,
    lost_list,
    ordered_list,
    sold_list,
    starting_list,
):
    import pandas as pd

    table_40 = pd.DataFrame({
        "Day": range(1, len(daily_demand) + 1),
        "Starting Stock": starting_list,
        "Arrived": arrived_list,
        "Demand": demand_list,
        "Sold": sold_list,
        "Lost": lost_list,
        "Ending Stock": ending_list,
        "Units Ordered": ordered_list
    })

    table_40
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(
    daily_demand,
    lead_time_days,
    order_quantity,
    pd,
    reorder_points,
    starting_stock,
):
    summary_points = []
    summary_units_lost = []
    summary_lost_days = []
    summary_orders_placed = []
    summary_avg_ending = []

    for rp in reorder_points:
        cur_stock = starting_stock
        due_day = -1
        total_lost = 0
        lost_day_count = 0
        orders_count = 0
        ending_sum = 0

        for day_i in range(len(daily_demand)):
            day_arrived = 0
            if due_day == day_i:
                cur_stock = cur_stock + order_quantity
                day_arrived = order_quantity
                due_day = -1

            day_demand = daily_demand[day_i]
            if cur_stock >= day_demand:
                day_sold = day_demand
                day_lost = 0
            else:
                day_sold = cur_stock
                day_lost = day_demand - day_sold

            cur_stock = cur_stock - day_sold
            total_lost = total_lost + day_lost
            if day_lost > 0:
                lost_day_count = lost_day_count + 1

            if cur_stock <= rp and due_day == -1:
                due_day = day_i + lead_time_days
                orders_count = orders_count + 1

            ending_sum = ending_sum + cur_stock

        average_ending = ending_sum / len(daily_demand)

        summary_points.append(rp)
        summary_units_lost.append(total_lost)
        summary_lost_days.append(lost_day_count)
        summary_orders_placed.append(orders_count)
        summary_avg_ending.append(average_ending)

    table_reorder_compare = pd.DataFrame({
        "Reorder Point": summary_points,
        "Units Lost": summary_units_lost,
        "Days With Lost Sale": summary_lost_days,
        "Orders Placed": summary_orders_placed,
        "Average Ending Stock": summary_avg_ending
    })

    table_reorder_compare
    return summary_avg_ending, summary_units_lost


@app.cell
def _(reorder_points, summary_avg_ending, summary_units_lost):
    print(
        f"The reorder point that is the most ideal is "
        f"{reorder_points[2]}. There were {summary_units_lost[2]} units lost, "
        f"and the average ending stock was around "
        f"{summary_avg_ending[2]:.1f} units. "
        f"Any lower reorder points like "
        f"{reorder_points[0]} or {reorder_points[1]} would result in more units lost, "
        f"while any higher like {reorder_points[3]} would "
        f"increase the average ending stock without significantly reducing lost units."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(demand_list, lost_list, sold_list):
    total_demand = sum(demand_list)
    total_sold_and_lost = sum(sold_list) + sum(lost_list)

    print(total_demand)
    print(total_sold_and_lost)
    print(total_demand == total_sold_and_lost) 
    return


@app.cell
def _(daily_demand):
    sum(daily_demand)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every unit of demand each day either gets sold or gets lost, so the 2 totals must match if the code was correct. The concepts I used was values and names, lists, and sum and print statements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It added the f string, and it assumed there was a [4] reorder point, and it only went up to [3].
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The agent got the tables right on the second try. The first try, the agent only made a table for 40 reorder points, so when I was trying to compare with the other reorder points, like 20, 30 and 50, it was not calculating. I had to point out that the comparison required reorder points across the full range, not just one value, before the agent regenerated the tables correctly.

    After clarifying the requirement, the agent correctly regenerated the tables with reorder points of 20, 30, 40, and 50, allowing for a proper side-by-side comparison. This highlighted the importance of being explicit about the full scope of parameters needed when requesting comparative analysis, rather than assuming the agent would infer the complete range from context.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _():
    # COST 
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, pd, starting_stock):
    _cost_points = []
    _cost_total_lost = []
    _cost_orders_placed = []
    _cost_holding_sum = []
    _cost_total = []

    for _rp in range(10, 81, 10):
        _cur_stock = starting_stock
        _due_day = -1
        _total_lost = 0
        _orders_count = 0
        holding_sum = 0

        for _day_i in range(len(daily_demand)):
            if _due_day == _day_i:
                _cur_stock = _cur_stock + order_quantity
                _due_day = -1

            _day_demand = daily_demand[_day_i]
            if _cur_stock >= _day_demand:
                _day_sold = _day_demand
                _day_lost = 0
            else:
                _day_sold = _cur_stock
                _day_lost = _day_demand - _day_sold

            _cur_stock = _cur_stock - _day_sold
            _total_lost = _total_lost + _day_lost

            if _cur_stock <= _rp and _due_day == -1:
                _due_day = _day_i + lead_time_days
                _orders_count = _orders_count + 1

            holding_sum = holding_sum + _cur_stock

        holding_cost = 0.50 * holding_sum
        delivery_cost = 40 * _orders_count
        lost_margin_cost = 8 * _total_lost
        total_cost = holding_cost + delivery_cost + lost_margin_cost

        _cost_points.append(_rp)
        _cost_total_lost.append(_total_lost)
        _cost_orders_placed.append(_orders_count)
        _cost_holding_sum.append(holding_sum)
        _cost_total.append(total_cost)

    _table_cost_compare = pd.DataFrame({
        "Reorder Point": _cost_points,
        "Units Lost": _cost_total_lost,
        "Orders Placed": _cost_orders_placed,
        "Carton-Nights in Fridge": _cost_holding_sum,
        "Total Cost ($)": _cost_total
    })

    _table_cost_compare

    best_cost = _cost_total[0]
    best_point = _cost_points[0]

    for k in range(len(_cost_points)):
        if _cost_total[k] < best_cost:
            best_cost = _cost_total[k]
            best_point = _cost_points[k]

    print(f"The lowest-cost reorder point is {best_point}, costing ${best_cost:.2f} over the 30 days.")
    _table_cost_compare
    return


@app.cell
def _(lead_time_days, order_quantity, starting_stock):
    import random

    random.seed(42)

    year_demand = []
    for _ in range(365):
        year_demand.append(random.randint(8, 20))

    year_stock = starting_stock
    year_due_day = -1
    year_total_lost = 0
    year_lost_days = 0
    year_ending_sum = 0

    for yr_day_i in range(len(year_demand)):
        if year_due_day == yr_day_i:
            year_stock = year_stock + order_quantity
            year_due_day = -1

        yr_day_demand = year_demand[yr_day_i]
        if year_stock >= yr_day_demand:
            yr_day_sold = yr_day_demand
            yr_day_lost = 0
        else:
            yr_day_sold = year_stock
            yr_day_lost = yr_day_demand - yr_day_sold

        year_stock = year_stock - yr_day_sold
        year_total_lost = year_total_lost + yr_day_lost
        if yr_day_lost > 0:
            year_lost_days = year_lost_days + 1

        if year_stock <= 40 and year_due_day == -1:
            year_due_day = yr_day_i + lead_time_days

        year_ending_sum = year_ending_sum + year_stock

    year_avg_ending = year_ending_sum / len(year_demand)

    print(f"Over 365 random days with reorder point 40:")
    print(f"Units lost: {year_total_lost}")
    print(f"Days with a lost sale: {year_lost_days} out of {len(year_demand)}")
    print(f"Average ending stock: {year_avg_ending:.1f}")
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    reorder_point_slider = mo.ui.slider(10, 80, value=40, step=5, label="Reorder point")
    reorder_point_slider
    return (reorder_point_slider,)


@app.cell
def _(
    alt,
    daily_demand,
    lead_time_days,
    order_quantity,
    pd,
    reorder_point_slider,
    starting_stock,
):
    _stock = starting_stock
    _due_day = -1
    _ending_list = []

    for _i in range(len(daily_demand)):
        if _due_day == _i:
            _stock = _stock + order_quantity
            _due_day = -1

        _demand = daily_demand[_i]
        if _stock >= _demand:
            _sold = _demand
        else:
            _sold = _stock

        _stock = _stock - _sold

        if _stock <= reorder_point_slider.value and _due_day == -1:
            _due_day = _i + lead_time_days

        _ending_list.append(_stock)

    _chart_df = pd.DataFrame({
        "Day": range(1, len(daily_demand) + 1),
        "Ending Stock": _ending_list
    })

    _stock_line = alt.Chart(_chart_df).mark_line(point=True).encode(
        x=alt.X("Day", title="Day"),
        y=alt.Y("Ending Stock", title="Ending Stock (cartons)"),
        tooltip=["Day", "Ending Stock"]
    ).properties(
        title=f"Stock Over 30 Days (Reorder Point = {reorder_point_slider.value})",
        width=600,
        height=300
    )

    _reorder_rule = alt.Chart(pd.DataFrame({"y": [reorder_point_slider.value]})).mark_rule(
        color="red", strokeDash=[4, 4]
    ).encode(y="y")

    _stock_line + _reorder_rule
    return


@app.cell
def _(
    daily_demand,
    lead_time_days,
    order_quantity,
    pd,
    reorder_point_slider,
    starting_stock,
):
    import altair as alt

    _stock = starting_stock
    _due_day = -1
    _ending_list = []


    for _i in range(len(daily_demand)):
        if _due_day == _i:
            _stock = _stock + order_quantity
            _due_day = -1

        _demand = daily_demand[_i]
        if _stock >= _demand:
            _sold = _demand
        else:
            _sold = _stock

        _stock = _stock - _sold

        if _stock <= reorder_point_slider.value and _due_day == -1:
            _due_day = _i + lead_time_days

        _ending_list.append(_stock)

    _chart_df = pd.DataFrame({
        "Day": range(1, len(daily_demand) + 1),
        "Ending Stock": _ending_list
    })

    _stock_line = alt.Chart(_chart_df).mark_line(point=True).encode(
        x=alt.X("Day", title="Day"),
        y=alt.Y("Ending Stock", title="Ending Stock (cartons)"),
        tooltip=["Day", "Ending Stock"]
    ).properties(
        title=f"Stock Over 30 Days (Reorder Point = {reorder_point_slider.value})",
        width=600,
        height=300
    )

    _reorder_rule = alt.Chart(pd.DataFrame({"y": [reorder_point_slider.value]})).mark_rule(
        color="red", strokeDash=[4, 4]
    ).encode(y="y")

    _stock_line + _reorder_rule
    return (alt,)


if __name__ == "__main__":
    app.run()
