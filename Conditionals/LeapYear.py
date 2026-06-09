#   Checking for leap year
#   so logic is the year should be divisible by 4 but not by 100, also either that or should be divisible by 400

year = int(input("Enter a year: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} is a leap year")
else:
    print(f"{year} is NOT a leap year")