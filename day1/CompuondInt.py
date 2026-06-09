#   Program to calculate Compound interest

# formula for compound interest is principle * (1 + (rate / number of times interest is compounded per annum{n})) ^ n*time invested or borrowed
#   if intrest calculated only once a year then formula simplifies into p * (1 + r) ^ t

P = float(input("Enter the principle amount: "))
r = float(input("Enter the rate of interest: "))
n = int(input("Enter number of times compounded per annum (default 1 for once a year)"))
t = float(input("Enter the number of year for interest"))


A = P * ((1 + r / n) ** (n * t))
interest = A - P

print(f"Total amount is {A:.2f} with interest of{interest:.2f}")