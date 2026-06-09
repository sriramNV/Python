#   Program to find largest of three number
n1 = int(input("First Number: "))
n2 = int(input("Second Number: "))
n3 = int(input("Third Number: "))

if n1 > n2:
    if n1 > n3:
        print(f"{n1} is the greatest of three")
    else:
        print(f"{n3} is the greatest of three")
elif n2 > n3:
    print(f"{n2} is the greatest of three")
else:
    print(f"{n3} is the greatest of three")