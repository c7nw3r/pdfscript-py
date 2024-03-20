def iterate(array: list):
    for i, item in enumerate(array):
        yield i == 0, i == len(array) - 1, item


def flatten(array):
    return [item for sublist in array for item in sublist]
