#   Program to swap two variable values without third variable

n1 = int(input("Enter number 1: ")) 
n2 = int(input("Enter number 2: ")) 

n1 = n1 + n2 
n2 = n1 - n2 
n1 = n1 - n2 

print(f"First variable is {n1} and second variable is {n2}")

# python also has set operation that does it easily

n1, n2 = n2, n1
print(n1, n2)