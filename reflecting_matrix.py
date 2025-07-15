import numpy as np

def gsBasis(A):
    """
    Perform Gram-Schmidt orthonormalization on the columns of A
    to produce an orthonormal basis.
    """
    B = np.zeros_like(A, dtype=np.float64)
    for i in range(A.shape[1]):
        vec = A[:, i]
        for j in range(i):
            vec -= np.dot(B[:, j], A[:, i]) * B[:, j]
        norm = np.linalg.norm(vec)
        if norm < 1e-14:
            B[:, i] = 0
        else:
            B[:, i] = vec / norm
    return B

def build_reflection_matrix(bearBasis):
    """
    Given a 2x2 basis matrix (bearBasis), build the 2D reflection matrix
    over the mirror aligned with the first vector in that basis.
    """
    # Step 1: Get orthonormal basis aligned with mirror
    E = gsBasis(bearBasis)

    # Step 2: Define reflection in mirror's coordinates
    TE = np.array([[1, 0],
                   [0, -1]])

    # Step 3: Transform back to standard coordinates
    T = E @ TE @ E.T

    return T

if __name__ == "__main__":
    # Example: Reflect across the line y = x
    bearBasis = np.array([[1, 1],
                          [1, -1]]).T

    print("Bear's Basis:")
    print(bearBasis)

    reflection_matrix = build_reflection_matrix(bearBasis)
    print("\nReflection Matrix T:")
    print(reflection_matrix)

    # Test reflection of a vector
    v = np.array([1, 2])
    reflected_v = reflection_matrix @ v

    print("\nOriginal vector:", v)
    print("Reflected vector:", reflected_v)
