def gcd(a, b):
    """
    Find the greatest common divisor of two numbers using Euclidean algorithm.
    """
    while b:
        a, b = b, a % b
    return a


# Example usage
num1 = 3439348
num2 = 234882397
result = gcd(num1, num2)
print(f"GCD of {num1} and {num2} is {result}")