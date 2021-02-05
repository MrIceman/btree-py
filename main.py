def fibonacci(n):
    if n == 0 or n == 1:
        return 1
    a = fibonacci(n - 2)
    b = fibonacci(n - 1)
    return a + b


for i in range(0, 10):
    print(f'{i}: {fibonacci(i)}')
