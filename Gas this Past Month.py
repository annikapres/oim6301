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
    What is the amount of money that I have spent on gas over the past month, August 15 to September 15?
    """)
    return


@app.cell
def _():
    august = [35.89,40.56,44.55]
    september = [39.20,49.00,40.39,34.00]
    return


@app.cell
def _():
    gas_money = [ 35.89,40.56,44.55,39.20,49.00,40.39,34.00]
    print(gas_money)
    return (gas_money,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A single number is the price of gas for one trip to the gas station.
    """)
    return


@app.cell
def _(gas_money):
    total = sum(gas_money)
    print(total)
    return (total,)


@app.cell
def _(gas_money):
    times_went = len(gas_money)
    print(times_went)
    return (times_went,)


@app.cell
def _(times_went, total):
    average = total/times_went
    print(average)
    return (average,)


@app.cell
def _():
    35.89+40.56+44.55+39.20+49.00+40.39+34.00
    return


@app.cell
def _():
    283.59/7
    return


@app.cell
def _(average, times_went, total):
    print(f"I went to get gas {times_went} times this month, with the average cost being ${average:.2f} and the total was ${total:.2f}.")
    return


if __name__ == "__main__":
    app.run()
