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
    I need to look at the website to see the middlesex county and all the towns in it. Using the python get. would help me to find the towns from the api. Then a for loop for all the towns to see if they are under budget.
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return


if __name__ == "__main__":
    app.run()
