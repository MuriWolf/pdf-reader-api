import math

def create_int_interval(initial_number: int, last_number: int) -> list[int]:
    numbers = []

    for n in range(abs(last_number - initial_number) + 1):
        numbers.append(initial_number + n)

    return numbers