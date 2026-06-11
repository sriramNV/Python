#   used Sieve of Eratosthenes

n = int(input("Enter N: "))

if n < 2:
    print(f'kindly give a number greater than 2')
else:
    is_prime = [True] * (n + 1)                     #   populating an array of given size as true
    is_prime[0] = is_prime[1] = False               #   populating index 0 and 1 as false as 0 and 1 are not prime not constants

    p = 2                                           #   starting from 2
    while p * p <= n:                               #   since we just need to check till square root of n
        if is_prime[p]:                             #   checking if the given index num is prime
            for multiple in range(p*p, n+1, p):     #   marking all the multiples of p as not prime in the populated array
                is_prime[multiple] = False          #   marking all the multiples of p as not prime in the populated array
        p += 1                                      #   incrementing
    
    for i in range(2, n+1):
        if is_prime[i]:
            print(i)

    