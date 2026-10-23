import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import requests
    import json
    import csv
    import polars as pl

    return pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1. Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool would help people when they are looking to buy a house and they wanted to find a home that fits their budget while keeping property taxes affordable. It helps them decide which towns to consider when buying a home by comparing average home values and annual property tax bills.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. My Plan Before AI. Before you ask your agent anything, open the API's address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:

    - Which functions will your tool need? For each, what goes in and what comes out?

    - Which addresses will they request?

    - How will you know you have every record?

    - Which check will you use in section 6, and which two numbers should agree?

    - Commit with the message mp2: plan before AI.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I need to look at the website to see the middlesex county and all the towns in it. I would use each town's code to get its property tax information for fiscal year 2026. I would then compare each town's average home value to the $700,000 budget and its average property tax bill to the $8,000 limit. I would then rank them by lowest price and lowest average tax bill to find the best towns that fit within both budgets. Also save this information to a CSV file so I can access it later without having to call the API again.

    The tools I will need: dictionary, lists, get., for loops, if statements, CSV writing, f-strings, sorting.

    Using the python get. would help me to find the towns from the api. Then a for loop for all the towns to see if they are under budget. I would use dictionaries and lists to store the town information and if statements to check which towns meet both limits. Then I would print the list of towns that meet both criteria, along with their corresponding data, making sure its sorted by average tax bill from lowest to highest. Then show the results in a table with the town name, average home value, residential tax rate, and average bill. ALso save the collected data to a CSV file and use an f-string to write a sentence summarizing the results.

    I will create a function that takes a town’s dor_code and fiscal year and returns its tax history records. I will address the: /ma/towns?county=Middlesex to get the towns and /ma/towns/{dor_code}/history to get each town’s tax information.

    I will check the API’s information to find the total number of towns and make sure I set the pagination to 100 towns per page.


    To check in section 6, I will calculate the total number of towns that meet both the home price and property tax limits in two different ways: by counting the filtered list and by counting the towns that meet both conditions in a separate for loop. The two numbers should agree to confirm that my filtering is correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. Inputs. Every input in one cell.
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. The Work. Your functions, and the code that uses them.

    A couple is looking for a single-family home in Middlesex County with a budget of $700,000, and they want to keep the property tax bill under $8,000 a year. They want a short list of towns where the average home fits the budget and the average bill fits the limit, cheapest bill first, and they want to rerun it for another county or another budget.

    The data is the course API's Massachusetts endpoints, built from the state's Division of Local Services: oim.zhili.dev/ma lists them, and oim.zhili.dev/docs describes every field.

    The main task

    - Every town in the county, from /ma/towns?county=.... The reply's pagination reports how many towns there are; make sure you have all of them.
    - For each town, its figures for fiscal_year from /ma/towns/{dor_code}/history. Compare every town for the same year.
    - A table of the towns that pass both limits, cheapest bill first: town, average home value, residential tax rate, and average bill.
    - One sentence that answers the couple, with the numbers in it.
    - You may need the params= argument of requests.get. A page holds 50 towns unless you ask for more, up to 100.
    """)
    return


@app.cell
def _(county, requests):
    response = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": county, "per_page": 100},
    )
    data = response.json()
    data
    return (data,)


@app.cell
def _(data):
    pagination_total = data["pagination"]["total"]
    return (pagination_total,)


@app.cell
def _(requests):
    _probe = requests.get(
        "https://oim.zhili.dev/ma/towns/002/history",
    )
    _probe.json()
    return


@app.cell
def _(data, fiscal_year, requests):
    town_records = []
    towns_without_year = 0

    for town in data["items"]:
        history_response = requests.get(
            f"https://oim.zhili.dev/ma/towns/{town['dor_code']}/history"
        )
        history = history_response.json()

        found_year = False
        for year_record in history["years"]:
            if year_record["fiscal_year"] == fiscal_year:
                found_year = True
                town_records.append({
                    "name": town["name"],
                    "average_value": year_record["average_single_family_value_dollars"],
                    "tax_rate": year_record["residential_rate_per_thousand"],
                    "average_bill": year_record["average_single_family_bill_dollars"],
                })

        if not found_year:
            towns_without_year = towns_without_year + 1

    town_records
    return (town_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_records):
    affordable_towns = []

    for record in town_records:
        if record["average_value"] <= budget_dollars and record["average_bill"] <= tax_limit_dollars:
            affordable_towns.append(record)

    affordable_towns.sort(key=lambda record: record["average_bill"])

    affordable_towns
    return (affordable_towns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The Answer. Your result table, printed with print and f-strings with the columns lined up, and one sentence that answers the question in section 1 with the numbers in it. Print the sentence from code with an f-string, so that it changes when the data does.
    """)
    return


@app.cell
def _(affordable_towns):
    print(f"{'Name':<15}{'Average Value':>15}{'Tax Rate':>10}{'Average Bill':>15}")
    for _record in affordable_towns:
        print(
            f"{_record['name']:<15}"
            f"{_record['average_value']:>15,}"
            f"{_record['tax_rate']:>10}"
            f"{_record['average_bill']:>15,}"
        )
    return


@app.cell
def _(affordable_towns, pagination_total):
    f"Of the {pagination_total} Middlesex towns, those meeting both limits are sorted cheapest bill first \u2014 " \
    f"{affordable_towns[0]['name']} (${affordable_towns[0]['average_bill']:,}) and {affordable_towns[1]['name']} (${affordable_towns[1]['average_bill']:,}) are at the top, {affordable_towns[-2]['name']} (${affordable_towns[-2]['average_bill']:,}) and {affordable_towns[-1]['name']} (${affordable_towns[-1]['average_bill']:,}) near the bottom of the list."
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Going Further: Show how the bill has changed over 10 years for the three towns with the lowest bill on your list.
    """)
    return


@app.cell
def _(affordable_towns):
    # Find the three towns with the lowest average bill on our affordable list
    cheapest_three_names = []
    for _record in affordable_towns[:3]:
        cheapest_three_names.append(_record["name"])

    cheapest_three_names
    return (cheapest_three_names,)


@app.cell
def _(cheapest_three_names, data):
    # Get the dor_code for each of the three cheapest towns
    cheapest_three_codes = []
    for _town in data["items"]:
        if _town["name"] in cheapest_three_names:
            cheapest_three_codes.append(_town["dor_code"])

    cheapest_three_codes
    return (cheapest_three_codes,)


@app.cell
def _(cheapest_three_codes, fiscal_year, requests):
    # Pull 10 years of bill history (fiscal_year - 9 through fiscal_year) for the three cheapest towns
    start_year = fiscal_year - 9

    bill_history = []
    missing_year_count = 0

    for code in cheapest_three_codes:
        _history_response = requests.get(f"https://oim.zhili.dev/ma/towns/{code}/history")
        _town_history = _history_response.json()

        for _year_record in _town_history["years"]:
            if _year_record["fiscal_year"] >= start_year and _year_record["fiscal_year"] <= fiscal_year:
                if _year_record["average_single_family_bill_dollars"] is None:
                    missing_year_count = missing_year_count + 1
                else:
                    bill_history.append({
                        "name": _town_history["name"],
                        "fiscal_year": _year_record["fiscal_year"],
                        "average_bill": _year_record["average_single_family_bill_dollars"],
                    })

    bill_history
    return (bill_history,)


@app.cell
def _(bill_history, pl):
    bill_history_table = pl.DataFrame(bill_history)
    bill_history_table
    return (bill_history_table,)


@app.cell
def _(bill_history_table):
    import altair as alt

    bill_chart = alt.Chart(bill_history_table).mark_line(point=True).encode(
        x=alt.X("fiscal_year:O", title="Fiscal year"),
        y=alt.Y("average_bill:Q", title="Average tax bill ($)"),
        color=alt.Color("name:N", title="Town"),
        tooltip=["name", "fiscal_year", "average_bill"],
    ).properties(
        title="10-year tax bill trend: three cheapest affordable towns",
        width=500,
        height=300,
    )
    bill_chart
    return


@app.cell
def _(bill_history, cheapest_three_names, fiscal_year):
    # For each of the three cheapest towns, compare the bill 3 years ago to the current bill
    three_years_ago = fiscal_year - 3

    for _name in cheapest_three_names:
        _old_bill = None
        _new_bill = None

        for _record in bill_history:
            if _record["name"] == _name and _record["fiscal_year"] == three_years_ago:
                _old_bill = _record["average_bill"]
            if _record["name"] == _name and _record["fiscal_year"] == fiscal_year:
                _new_bill = _record["average_bill"]

        if _old_bill is None or _new_bill is None:
            print(f"{_name}: not enough history to compare {three_years_ago} to {fiscal_year}.")
        else:
            _dollar_change = _new_bill - _old_bill
            _percent_change = _dollar_change / _old_bill * 100
            print(
                f"{_name}'s average bill went from ${_old_bill:,} in fiscal year {three_years_ago} "
                f"to ${_new_bill:,} in fiscal year {fiscal_year}, "
                f"a rise of ${_dollar_change:,} ({_percent_change:.1f}%)."
            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. How I Know These Numbers Are Right. Reach at least one result a second way, in this notebook, and show that the two agree. Write a cell that gets the same number from other fields, or open the raw reply in your browser and find each number of one row of your table there. For instance: an average bill is close to the average value times the tax rate divided by 1,000; an order's total equals the sum of its lines; the number of records you collected equals the total the API reports. At least one of those checks runs as code, and shows both numbers.
    """)
    return


@app.cell
def _(county, pagination_total, town_records):
    # Check 1: does the number of towns we collected match what the API says exists?
    collected_count = len(town_records)

    print(f"Towns collected: {collected_count}")
    print(f"Towns the API reports for {county}: {pagination_total}")
    print(f"These agree: {collected_count == pagination_total}")
    return


@app.cell
def _(affordable_towns):
    # Check 2: for one town on our list, does average value * tax rate / 1,000 come out close to the reported average bill?
    check_town = affordable_towns[0]

    calculated_bill = check_town["average_value"] * check_town["tax_rate"] / 1000
    reported_bill = check_town["average_bill"]

    print(f"Town: {check_town['name']}")
    print(f"Average value: ${check_town['average_value']:,}")
    print(f"Tax rate: {check_town['tax_rate']} per $1,000")
    print(f"Calculated bill (value \u00d7 rate / 1000): ${calculated_bill:,.0f}")
    print(f"Reported bill from the API: ${reported_bill:,}")
    print(f"These are close: {abs(calculated_bill - reported_bill) < 50}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. Working With the Agent. Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: What did you do to verify that? Pointing to your check in section 6 is enough.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    AI originally gave me a table not using print but pl. ,but I asked it to format the output using print and f-strings instead. This was a polars table built from pl. similar to notebook 5, but section 5 asked for the result printed with print and f-strings, with the columns lined up \u2014 a polars table display doesn't satisfy that. I asked the AI to redo it that way, and it added a new cell that uses print() with :<15 and :>15 alignment codes to line up the Name, Average Value, Tax Rate, and Average Bill columns.

    I knew the first version wasn't acceptable because the instructions explicitly named print and f-strings as the required tools, and a pl.DataFrame table is a different mechanism. Comparing the printed numbers to the table output confirmed both showed the same 12 towns and values, just formatted differently so the fix only changed the display, not the underlying data.

    The main loop that pulls every town's history and filters by budget and tax limit, was correct the first time and I didn't have to change the logic. To verify that, I used the check in section 6 to count the towns I collected with len(town_records) and compares that to pagination_total, the total the API itself reports for Middlesex. Both came out to 54, so I know the loop wasn't silently skipping or duplicating any towns. I also calculated the calculated bill= average value * tax rate / 1,000. This number was the same as the reported bill from API, which also confirmed the numbers lined up.
    """)
    return


if __name__ == "__main__":
    app.run()
