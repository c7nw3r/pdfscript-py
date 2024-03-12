def iterate(array: list):
    for i, item in enumerate(array):
        yield i == 0, i == len(array) - 1, item
