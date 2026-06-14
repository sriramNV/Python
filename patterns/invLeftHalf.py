#   Printing inverted right half triangle for given input N

n = int(input("enter N: "))

for i in range(1,n + 1):
    print(" " * (i-1), "*" * (n-i+1))