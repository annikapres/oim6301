# import bmi

people = [
	{"name": "Avery", "height": 1.68, "weight": 62},
	{"name": "Jordan", "height": 1.82, "weight": 78},
	{"name": "Casey", "height": 1.59, "weight": 54},
	{"name": "Morgan", "height": 1.74, "weight": 70},
	{"name": "Riley", "height": 1.91, "weight": 86},
	{"name": "Taylor", "height": 1.65, "weight": 59},
	{"name": "Quinn", "height": 1.77, "weight": 73},
	{"name": "Hayden", "height": 1.71, "weight": 67},
]

# result = bmi.compute_bmi(70, 1.75)
# print(f"Computed BMI: {result:.2f}")

for person in people:
    print(person)

for height in people:
    print(height["height"])

person["height"]


# for person in people:
# 	bmi_value = bmi.compute_bmi(person["weight"], person["height"])
# 	category = bmi.get_bmi_category(bmi_value)
# 	print(f"{person['name']}: {category}")



