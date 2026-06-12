num = int(input("Enter a number: "))

temp = num
sum = 0
while num > 0:
    d = num % 10
    sum = (sum * 10) + d
    num = num // 10
    # print(num)
print(sum)


