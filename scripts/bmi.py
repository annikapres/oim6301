bmi = 27


def compute_bmi(weight, height):
    bmi= weight / (height ** 2)
    return bmi


# wrap this code in a function
def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    #print(category)
    return category
    
# classify_bmi(bmi) #only refers to bmi in line 1, not the function parameter bmi
# print(bmi) #prints 27, not the category

# bmi=18
# result = classify_bmi(bmi)
# print(f"Your category is {result}.")

def main():
    weight = float(input("Enter your weight in kilograms: "))
    height = float(input("Enter your height in meters: "))
    bmi = compute_bmi(weight, height)
    result = classify_bmi(bmi)
    print(f"Your BMI is {bmi:.2f}, which is classified as {result}.")

main()


if __name__ == "__main__":
    main()



