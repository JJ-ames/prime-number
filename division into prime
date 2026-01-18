def prime_factorization(n):
    """
    Returns a list of prime factors of n.
    """
    factors = []  # Initialize an empty list to store prime factors
    d = 2  # Start checking for factors from the smallest prime number, 2
    
    while d * d <= n:  # Continue while d squared is less than or equal to n
        while n % d == 0:  # Check if d is a factor of n
            factors.append(d)  # If it is, add d to the factors list
            n //= d  # Divide n by d to reduce n
        d += 1  # Move to the next potential factor
    
    if n > 1:  # If n is still greater than 1, it must be prime
        factors.append(n)  # Add the remaining prime factor to the list
    
    return factors  # Return the list of prime factors


# Example usage
number = 234
result = prime_factorization(number)
print(f"Prime factors of {number}: {result}")