def fibo_sumN (term):
    x1 = 0
    x2 = 1
    result = 0
    while term >= 0:
        result += x1
        x3 = x1 + x2
        x1 = x2
        x2 = x3
        term -= 1
    return result
print("Sum of the first 5 terms of the Fibonacci series:", fibo_sumN(5), "\nSum of the first 10 terms of the Fibonacci series:", fibo_sumN(10))