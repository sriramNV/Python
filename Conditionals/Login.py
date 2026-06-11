#   Basic login system with hardcoded values

hpassw = '*123!!!acdabc'
huser = 'admin'

user = input("Enter your user name: ")
if user == huser:
    passw = input("Enter your password: ")
    if passw == hpassw:
        print("YOU ARE LOGGED IN")
    else:
        print("ERROR!!! WRONG PASSWORD")
else:
    print("ERROR!!! WRONG USER")