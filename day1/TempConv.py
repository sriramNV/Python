#   The first exercise to convert the given temparature from celsius to farenheit

cel = float(input("Enter the temparature in Celsius: "))
farenheit = (cel * float(9 / 5)) + 32
print(f"The {cel} degree celsius is {farenheit:.2f} degree farenheit")