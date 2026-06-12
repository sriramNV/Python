num = int(input("Enter a number: "))
length = len(str(num))

sum = 0

temp = num

while num > 0:
    d = num % 10
    sum = sum + (d ** length)
    num = num // 10
    print(sum)

if sum == temp:
    print(f'{temp} is an ARMSTRONG number')
else:
    print(f"{temp} is NOT an ARMSTRONG number")