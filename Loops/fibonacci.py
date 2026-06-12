# Fibonacci sequence generator upto given number(it generates upto 8 if given input is 10 since the next number in seq is 13 which is higher than 10)

SUm = 0
first = 1
second = 1
n = int (input("Enter N: "))
print(first)
print(second)
while (first + second) <= n:
    print(first + second)
    t = second
    second += first
    first = t

    