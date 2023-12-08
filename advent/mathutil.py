def gcd(m: int, n: int) -> int:
    """Return the greatest common divisor of m and n."""
    if n == 0:
        return m
    return gcd(n, m % n)


def lcm(m: int, n: int) -> int:
    """Return the least common multiple of m and n."""
    return abs(m * n) // gcd(m, n)
