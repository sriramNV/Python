#   BMI Calculator in kg and meter
#   BMI = weight / height 
#   category will be below 18.5 is underweight, upto 24.9 healthy w, upto 29.9 overweight, above 30 obese

weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in m: "))

BMI = weight / (height ** 2)
category = ""
if BMI <= 18.5:
    category = "Underweight"
elif BMI > 18.5 and BMI <= 24.9:
    category = "Healthy"
elif BMI > 25 and BMI <= 29.9:
    category = "Overweight"
elif BMI > 30:
    category = "Obese"
else:
    category = "INVALID CATEGORY"

if category != "INVALID CATEGORY":
    print(f"Your BMI is {BMI:.2f} and you are {category}")
else:
    print(f"{category} wrong height and weight")