#   Printing left half triangle for given input N

n = int(input("enter N: "))

for i in range(1,n + 1):
    print(" " * (n-i), "*" * (i))