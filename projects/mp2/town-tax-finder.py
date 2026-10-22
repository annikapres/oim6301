import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


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


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
