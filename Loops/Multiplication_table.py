#   printing multiplication table from 1 - 10

n = 11

for i in range(1,n):
    print(f"{i} times table \n")
    for j in range(1,11):
        print(f"{i} x {j} = {i*j}")
    print()
    print()
    