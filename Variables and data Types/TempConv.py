#   The first exercise to convert the given temparature from celsius to farenheit

inp = input("Enter the temparature with c/f (eg. 15c or 111f): ")

temp = int(inp[:-1])
deg = inp[-1]

if deg == 'c':
    farenheit = (temp * float(9 / 5)) + 32
    print(f"The {temp} degree celsius is {farenheit:.2f} degree farenheit")
elif deg == 'f':
    celsius = (temp - 32) * (5/9)
    print(f"The {temp} degree farenheit is {celsius:.2f} degree celius")
else:
    print("wrong temp")