import numpy as np

def pageRank(linkMatrix, d=0.85, max_iter=100, tol=1e-6):
    """
    Computes the PageRank vector using the power iteration method.

    Parameters:
    - linkMatrix: numpy.ndarray, the transition matrix (columns sum to 1)
    - d: float, damping factor (default 0.85)
    - max_iter: int, number of iterations to run (default 100)
    - tol: float, tolerance for convergence (default 1e-6)

    Returns:
    - r: numpy.ndarray, PageRank scores (not necessarily normalized)
    """
    n = linkMatrix.shape[0]
    r = np.ones(n) / n  # Initialize with equal rank
    M = d * linkMatrix + (1 - d) / n * np.ones((n, n))  # Google matrix

    for _ in range(max_iter):
        r_new = M @ r
        if np.linalg.norm(r_new - r, 1) < tol:
            break
        r = r_new

    return r


# Example Usage
if __name__ == "__main__":
    # Define the link matrix (column-stochastic)
    linkMatrix = np.array([
        [0,   0,   1, 0],
        [0.5, 0,   0, 0],
        [0.5, 0.5, 0, 1],
        [0,   0.5, 0, 0]
    ])

    # Compute PageRank
    d = 0.85  # Damping factor
    ranks = pageRank(linkMatrix, d)

    # Output the results
    print("PageRank scores:")
    for i, score in enumerate(ranks):
        print(f"Page {i}: {score:.4f}")
