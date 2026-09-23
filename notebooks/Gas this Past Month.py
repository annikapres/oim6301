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
    gas_money_raw = [35.89, 40.56, 44.55, 39.20, 49.00, 40.39, 34.00, "n/a"]
    return (gas_money_raw,)


@app.cell
def _():
    #couldnt run cuz there are floats adn str 
    return


@app.cell
def _(gas_money_raw):
    gas_money_clean = []
    for cost in gas_money_raw:
        if isinstance(cost, (int, float)):
            gas_money_clean.append(cost)

    print(gas_money_clean)
    return (gas_money_clean,)


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
    trips = len(gas_money)
    print(trips)
    return (trips,)


@app.cell
def _(total, trips):
    average = total/trips
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
def _(average, total, trips):
    print(f"I went to get gas {trips} times this month, with the average cost being ${average:.2f} and the total was ${total:.2f}.")
    return


@app.cell
def _(mo):
    extra_trips_slider = mo.ui.slider(
        0, 10, value=0, label="Additional gas trips planned this month"
    )
    extra_trips_slider
    return (extra_trips_slider,)


@app.cell
def _(average, extra_trips_slider, mo, total, trips):
    projected_trips = trips + extra_trips_slider.value
    projected_total = total + (extra_trips_slider.value * average)

    mo.md(
        f"I went to get gas {trips} times this past month, with the average cost "
        f"being ${average:.2f} and the total was ${total:.2f}. "
        f"If I make {extra_trips_slider.value} more trip(s) at the average cost, "
        f"I'll have gone {projected_trips} times and spent an estimated ${projected_total:.2f} total."
    )
    return


@app.cell
def _(average, gas_money_clean):
    import matplotlib.pyplot as plt

    labels = [f"Trip {i+1}" for i in range(len(gas_money_clean))]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, gas_money_clean, color="steelblue")
    plt.axhline(average, color="red", linestyle="--", label=f"Average (${average:.2f})")
    plt.title("Gas Spending by Trip")
    plt.xlabel("Trip")
    plt.ylabel("Cost ($)")
    plt.legend()
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Was there a trip that was under $35?
    """)
    return


@app.cell
def _(gas_money):
    under_35 =[]
    for money in gas_money:
        if money<35:
            under_35.append(money)
    print(under_35)
    return (under_35,)


@app.cell
def _():
    return


@app.cell
def _(under_35):
    print(f"Yes! there was one trip that was under $35, it was ${under_35}.")
    return


if __name__ == "__main__":
    app.run()
