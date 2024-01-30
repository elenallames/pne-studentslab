n_terms = 11
x1 = 0
x2 = 1
while n_terms > 0:
    print(x1, end=",")
    x3 = x1 + x2
    x1 = x2
    x2 = x3
    n_terms -= 1
