import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
	import marimo as mo
	from datetime import date

	return date, mo


@app.cell
def _(date):
	as_of = date(2026, 11, 11)
	return (as_of,)


@app.cell(hide_code=True)
def _(as_of, mo):
	mo.md(f"""
	# Babson Bean Cafe Database

	## 3. Reading It Back

	**Question:** BUSINESS Q #2 Revenue, cost and margin by menu category, with what the options earned counted in, each option under the category of the product on its line. (three tables or more)

	**Prediction:** Before grouping, I expect the joins from `orders` to `order_lines` to `products`, then through `line_options` to `options`, to produce about 2,000 rows. There are 1,000 orders with 1 to 3 lines each, averaging two lines per order. Each line must match one order and one product, and the line-options key allows at most one option per line, so left-joining options should preserve one row per order line. The selected `as_of` date is {as_of}.
	""")
	return
