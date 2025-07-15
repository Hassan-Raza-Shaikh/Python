import numpy as np
import numpy.linalg as la

verySmallNumber = 1e-14  # Tolerance for zero vector

# Gram-Schmidt for exactly 4 vectors
def gsBasis4(A):
    B = np.array(A, dtype=np.float_)

    # First vector
    B[:, 0] = B[:, 0] / la.norm(B[:, 0])

    # Second vector
    B[:, 1] = B[:, 1] - B[:, 1] @ B[:, 0] * B[:, 0]
    if la.norm(B[:, 1]) > verySmallNumber:
        B[:, 1] = B[:, 1] / la.norm(B[:, 1])
    else:
        B[:, 1] = np.zeros_like(B[:, 1])

    # Third vector
    B[:, 2] = B[:, 2] - B[:, 2] @ B[:, 0] * B[:, 0]
    B[:, 2] = B[:, 2] - B[:, 2] @ B[:, 1] * B[:, 1]
    if la.norm(B[:, 2]) > verySmallNumber:
        B[:, 2] = B[:, 2] / la.norm(B[:, 2])
    else:
        B[:, 2] = np.zeros_like(B[:, 2])

    # Fourth vector
    B[:, 3] = B[:, 3] - B[:, 3] @ B[:, 0] * B[:, 0]
    B[:, 3] = B[:, 3] - B[:, 3] @ B[:, 1] * B[:, 1]
    B[:, 3] = B[:, 3] - B[:, 3] @ B[:, 2] * B[:, 2]
    if la.norm(B[:, 3]) > verySmallNumber:
        B[:, 3] = B[:, 3] / la.norm(B[:, 3])
    else:
        B[:, 3] = np.zeros_like(B[:, 3])

    return B

# Generalized Gram-Schmidt for any number of vectors
def gsBasis(A):
    B = np.array(A, dtype=np.float_)
    for i in range(B.shape[1]):
        for j in range(i):
            B[:, i] = B[:, i] - B[:, i] @ B[:, j] * B[:, j]
        if la.norm(B[:, i]) > verySmallNumber:
            B[:, i] = B[:, i] / la.norm(B[:, i])
        else:
            B[:, i] = np.zeros_like(B[:, i])
    return B

# Computes the dimension of the space spanned by the column vectors
def dimensions(A):
    return np.sum(la.norm(gsBasis(A), axis=0) > verySmallNumber)

# ----------------------------
# Example usage and testing
# ----------------------------

if __name__ == "__main__":
    A = np.array([[1, 1, 1, 1],
                  [0, 1, 1, 1],
                  [0, 0, 1, 1],
                  [0, 0, 0, 1]], dtype=float)

    print("Original Matrix A:")
    print(A)

    print("\nOrthogonalized (gsBasis4):")
    print(gsBasis4(A))

    print("\nOrthogonalized (gsBasis):")
    print(gsBasis(A))

    print("\nDimension of span of A:")
    print(dimensions(A))  # Should print 4 since the vectors are linearly independent
