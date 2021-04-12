def calculateExpected(probability, places):
    """Calculate limit of probability function... probably a way to do it mathematically"""
    expectedValue = 0
    increase = 1
    tolerance = 0.1 ** places
    x = 1
    while increase > tolerance:
        increase = x * probability * (1 - probability) ** (x - 1)
        expectedValue += increase
        print("Iteration: {}, Expected: {}, Increase: {}".format(x, expectedValue, increase))
        x += 1
    return expectedValue


if __name__ == '__main__':
    print("Expected excerpt length = {} pixels".format(calculateExpected(1/3, 18)))

