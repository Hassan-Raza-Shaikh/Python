import numpy as lol

#Task 1

a = lol.zeros(10)
a[4] = 1
print(a)

#Task 2

matrix = lol.ones((4,4))
matrix[1:-1,1:-1] = 0
print(matrix)

#Task 3

array = lol.array(input().split(), dtype=float)

print(array[::-1])

#Task 4

numbers = lol.array([86.03331084,37.7285648,48.649080807,87.16563062,38.40852563,37.20006318])
if not isinstance(numbers, lol.ndarray) or numbers.ndim != 1:
        raise ValueError("Input must be a one-dimensional NumPy array")
exp_values = lol.exp(numbers - lol.max(numbers))

print(exp_values / exp_values.sum())


#Task 5

matrix = lol.random.randint(1, 10000, size=(8, 5))
alternate_columns = matrix[:, ::2]
print("Alternate Columns:\n", alternate_columns)
min_value, max_value = matrix.min(), matrix.max()
normalized_matrix = (matrix - min_value) / (max_value - min_value)
print("Normalized Matrix:\n", normalized_matrix)

#Task 6

target = 23
numbers = lol.array([10, 17, 24, 31, 38, 45, 52, 59])
closest_value = numbers[lol.abs(numbers - target).argmin()]
print("Nearest element:", closest_value)

#Task 7

matrix_with_nan = lol.array([[3, 2, lol.nan, 1],
                            [10, 12, 10, 9],
                            [5, lol.nan, 1, lol.nan]])

missing_values_mask = lol.isnan(matrix_with_nan)
print("Missing Data Matrix:\n", missing_values_mask)

filled_matrix = lol.nan_to_num(matrix_with_nan)
print("Matrix with NaNs replaced:\n", filled_matrix)