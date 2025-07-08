import numpy as np

# Check if the matrix is singular by trying to reduce it to echelon form
def isSingular(A):
    B = np.array(A, dtype=np.float_)
    try:
        fixRowZero(B)
        fixRowOne(B)
        fixRowTwo(B)
        fixRowThree(B)
    except MatrixIsSingular:
        return True
    return False

# Custom exception raised when a matrix is found to be singular
class MatrixIsSingular(Exception): pass

def fixRowZero(A):
    if A[0, 0] == 0:
        A[0] = A[0] + A[1]
    if A[0, 0] == 0:
        A[0] = A[0] + A[2]
    if A[0, 0] == 0:
        A[0] = A[0] + A[3]
    if A[0, 0] == 0:
        raise MatrixIsSingular()
    A[0] = A[0] / A[0, 0]
    return A

def fixRowOne(A):
    A[1] = A[1] - A[1, 0] * A[0]
    if A[1, 1] == 0:
        A[1] = A[1] + A[2]
        A[1] = A[1] - A[1, 0] * A[0]
    if A[1, 1] == 0:
        A[1] = A[1] + A[3]
        A[1] = A[1] - A[1, 0] * A[0]
    if A[1, 1] == 0:
        raise MatrixIsSingular()
    A[1] = A[1] / A[1, 1]
    return A

def fixRowTwo(A):
    A[2] = A[2] - A[2, 0] * A[0]
    A[2] = A[2] - A[2, 1] * A[1]
    if A[2, 2] == 0:
        A[2] = A[2] + A[3]
        A[2] = A[2] - A[2, 0] * A[0]
        A[2] = A[2] - A[2, 1] * A[1]
    if A[2, 2] == 0:
        raise MatrixIsSingular()
    A[2] = A[2] / A[2, 2]
    return A

def fixRowThree(A):
    A[3] = A[3] - A[3, 0] * A[0]
    A[3] = A[3] - A[3, 1] * A[1]
    A[3] = A[3] - A[3, 2] * A[2]
    if A[3, 3] == 0:
        raise MatrixIsSingular()
    A[3] = A[3] / A[3, 3]
    return A

# ===============================
# 🧪 Test the code with examples
# ===============================
if __name__ == "__main__":
    # Example 1: Non-singular matrix
    A1 = np.array([
        [2, 1, -1, -3],
        [1, 3, 2, 4],
        [1, -1, 2, -1],
        [3, 2, -3, 1]
    ])

    # Example 2: Singular matrix (row 4 is multiple of row 1)
    A2 = np.array([
        [1, 2, 3, 4],
        [0, 1, 2, 3],
        [0, 0, 1, 2],
        [1, 2, 3, 4]  # Same as row 1
    ])

    print("Matrix A1:")
    print(A1)
    print("Is A1 singular?", isSingular(A1))  # Expected: False

    print("\nMatrix A2:")
    print(A2)
    print("Is A2 singular?", isSingular(A2))  # Expected: True