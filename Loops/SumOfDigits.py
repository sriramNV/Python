#   program to count the number of digits in a given integer

num = int(input("Enter the number: "))

sum = 0

while num > 0:
    d = num % 10
    sum += d
    num = num // 10

print(f"Number of digits are: {sum}")