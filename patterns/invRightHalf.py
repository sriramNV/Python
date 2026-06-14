#   Printing inverted right half triangle for given input N

n = int(input("enter N: "))

for i in range(n,0,-1):
    print("* " * i)