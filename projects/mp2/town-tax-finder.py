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

    return (requests,)


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
    return


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
    return


app._unparsable_cell(
    r"""
    f'Of the {pagination_total} Middlesex towns, those meeting both limits are sorted cheapest bill first \u2014 
    {affordable_towns[0]['name']} (${affordable_towns[0]['average_bill']:,}) and {affordable_towns[1]['name']} (${affordable_towns[1]['average_bill']:,}) are at the top, {affordable_towns[-2]['name']} (${affordable_towns[-2]['average_bill']:,}) and {affordable_towns[-1]['name']} (${affordable_towns[-1]['average_bill']:,}) near the bottom of the list.'
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
