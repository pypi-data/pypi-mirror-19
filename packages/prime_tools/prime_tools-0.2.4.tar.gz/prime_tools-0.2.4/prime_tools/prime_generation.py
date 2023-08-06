def n_primes   ( n ):
    """Generates and returns the nth prime number"""

    from    math import sqrt

    primes = [2, 3]
    test_value = 5

    while len(primes) < n:
        isPrime = True
        for known_prime in primes:
            if known_prime > sqrt(test_value): 
                break
            elif test_value % known_prime == 0:
                isPrime = False

        if isPrime:
            primes.append(test_value)
        test_value += 2
        
    return primes



def nth_prime ( n ):
    return n_primes(n)[n - 1]
