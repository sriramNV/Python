#   Simple ATM withdrawal sim


balance = 1000


withdraw = int(input("Enter the amount to be withdrawn: "))
if withdraw > balance:
    print(f"Error!!! Insufficient Balance cannot withdraw amount:{withdraw} from balance:{balance}")
else:
    balance -= withdraw
    print(f"Withdrawal of amount:{withdraw} Successful, current balance:{balance}")