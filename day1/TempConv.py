#   The first exercise to convert the given temparature from celsius to farenheit

temp = float(input("Enter the temparature: "))
celsius = (temp - 32) * (5/9)
farenheit = (temp * float(9 / 5)) + 32
print(f"The {temp} degree celsius is {farenheit:.2f} degree farenheit")
print(f"The {temp} degree farenheit is {celsius:.2f} degree celius")