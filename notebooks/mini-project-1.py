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


@app.cell
def _():
    print("hi")

    return


@app.cell
def _():
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
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
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
