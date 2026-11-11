import csv
import random
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).parent / "data"
AS_OF = date(2026, 11, 11)
RANDOM_SEED = 6301

TABLE_COLUMNS = {
    "members": [
        "member_id",
        "first_name",
        "mobile_number",
        "email",
        "join_date",
        "points_balance",
    ],
    "products": [
        "product_id",
        "name",
        "category",
        "price",
        "cost",
        "is_available",
    ],
    "options": ["option_id", "name", "price", "cost"],
    "orders": ["order_id", "ordered_at", "member_id", "channel"],
    "order_lines": [
        "line_id",
        "order_id",
        "product_id",
        "quantity",
        "price_charged",
    ],
    "line_options": ["line_id", "option_id", "price_charged"],
    "payments": ["payment_id", "order_id", "method", "amount"],
}

PRODUCTS = [
    ("House Drip Coffee", "coffee", 275, 82, True),
    ("Espresso", "coffee", 250, 70, True),
    ("Americano", "coffee", 325, 96, True),
    ("Cappuccino", "coffee", 425, 148, True),
    ("Latte", "coffee", 450, 162, True),
    ("Mocha", "coffee", 500, 205, True),
    ("Cold Brew", "coffee", 475, 155, True),
    ("Chai Latte", "tea", 450, 172, True),
    ("Earl Grey", "tea", 300, 75, True),
    ("Matcha Latte", "tea", 525, 218, True),
    ("Hot Chocolate", "other", 425, 162, True),
    ("Blueberry Muffin", "food", 350, 125, True),
    ("Chocolate Croissant", "food", 400, 158, True),
    ("Avocado Toast", "food", 825, 365, True),
    ("Bagel with Cream Cheese", "food", 475, 188, True),
    ("Bottled Water", "other", 225, 65, True),
    ("Seasonal Scone", "food", 375, 140, True),
    ("Decaf Pour Over", "coffee", 375, 112, False),
    ("Peach Iced Tea", "tea", 400, 118, False),
    ("Granola Cup", "food", 525, 228, False),
]

OPTIONS = [
    ("Extra Espresso Shot", 90, 28),
    ("Oat Milk", 80, 35),
    ("Vanilla Syrup", 60, 12),
    ("Caramel Syrup", 60, 13),
    ("Whipped Cream", 50, 18),
    ("Almond Milk", 80, 38),
    ("Decaf Swap", 0, 8),
    ("Cinnamon", 0, 2),
]


def money(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def write_table(table_name, rows):
    file_path = DATA_DIR / f"{table_name}.csv"
    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=TABLE_COLUMNS[table_name])
        writer.writeheader()
        writer.writerows(rows)


def main():
    randomizer = random.Random(RANDOM_SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["members"] = []
    for member_id in range(1, 41):
        rows["members"].append(
            {
                "member_id": member_id,
                "first_name": f"Member{member_id:02d}",
                "mobile_number": f"555-010-{member_id:04d}",
                "email": f"member{member_id:02d}@example.test" if member_id % 4 else "",
                "join_date": AS_OF - timedelta(days=randomizer.randint(0, 900)),
                "points_balance": randomizer.randint(0, 800),
            }
        )

    rows["products"] = []
    for product_id, product in enumerate(PRODUCTS, start=1):
        name, category, price_cents, cost_cents, is_available = product
        rows["products"].append(
            {
                "product_id": product_id,
                "name": name,
                "category": category,
                "price": money(price_cents),
                "cost": money(cost_cents),
                "is_available": str(is_available).lower(),
            }
        )

    rows["options"] = []
    for option_id, option in enumerate(OPTIONS, start=1):
        name, price_cents, cost_cents = option
        rows["options"].append(
            {
                "option_id": option_id,
                "name": name,
                "price": money(price_cents),
                "cost": money(cost_cents),
            }
        )

    first_day = AS_OF - timedelta(days=364)
    weekdays = []
    weekend_days = []
    current_day = first_day
    while current_day <= AS_OF:
        if current_day.weekday() < 5:
            weekdays.append(current_day)
        else:
            weekend_days.append(current_day)
        current_day += timedelta(days=1)

    rows["orders"] = []
    rows["order_lines"] = []
    rows["line_options"] = []
    rows["payments"] = []
    next_line_id = 1
    next_payment_id = 1

    for order_id in range(1, 1001):
        if randomizer.random() < 0.86:
            order_day = randomizer.choice(weekdays)
        else:
            order_day = randomizer.choice(weekend_days)
        order_time = time(
            randomizer.choices(
                range(7, 18), weights=[2, 5, 9, 10, 8, 6, 5, 4, 5, 4, 2]
            )[0],
            randomizer.randrange(60),
        )

        member_id = None
        if randomizer.random() < 0.70:
            member_id = randomizer.randint(1, 39)
        rows["orders"].append(
            {
                "order_id": order_id,
                "ordered_at": datetime.combine(order_day, order_time),
                "member_id": member_id if member_id is not None else "",
                "channel": "app" if randomizer.random() < 0.28 else "counter",
            }
        )

        order_total_cents = 0
        line_count = randomizer.randint(1, 3)
        for line_number in range(line_count):
            if order_id <= 16 and line_number == 0:
                product_id = order_id
            else:
                product_id = randomizer.randint(1, 16)
            product = PRODUCTS[product_id - 1]
            quantity = randomizer.randint(1, 3)
            product_price = product[2]
            rows["order_lines"].append(
                {
                    "line_id": next_line_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "price_charged": money(product_price),
                }
            )
            order_total_cents += product_price * quantity

            if product[1] in ("coffee", "tea") and next_line_id % 3 != 0:
                if randomizer.random() < 0.58:
                    option_id = randomizer.randint(1, 7)
                    option_price = OPTIONS[option_id - 1][1]
                    rows["line_options"].append(
                        {
                            "line_id": next_line_id,
                            "option_id": option_id,
                            "price_charged": money(option_price),
                        }
                    )
                    order_total_cents += option_price * quantity
            next_line_id += 1

        if order_id == 1:
            continue
        if order_id == 2:
            order_total_cents -= 100

        payment_count = 2 if randomizer.random() < 0.18 else 1
        if payment_count == 1:
            payment_amounts = [order_total_cents]
            payment_methods = [randomizer.choice(["cash", "card", "app", "points"])]
        else:
            first_payment = randomizer.randint(1, order_total_cents - 1)
            payment_amounts = [first_payment, order_total_cents - first_payment]
            payment_methods = randomizer.sample(["cash", "card", "app", "points"], 2)

        for payment_method, payment_amount in zip(payment_methods, payment_amounts):
            rows["payments"].append(
                {
                    "payment_id": next_payment_id,
                    "order_id": order_id,
                    "method": payment_method,
                    "amount": money(payment_amount),
                }
            )
            next_payment_id += 1

    for table_name in TABLE_COLUMNS:
        write_table(table_name, rows[table_name])
        print(f"{table_name}: {len(rows[table_name])} rows")

    print("Payment-total exceptions: order_id 1 (no payment), order_id 2 ($1.00 short)")
    print(f"Orders cover {first_day} through {AS_OF}.")


if __name__ == "__main__":
    main()