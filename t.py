import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# --- 1. Data Generation ---
# Generate 200 random 2D points in 3 natural clusters using different means
cluster1 = np.random.randn(67, 2) + np.array([2, 2])
cluster2 = np.random.randn(67, 2) + np.array([8, 8])
cluster3 = np.random.randn(66, 2) + np.array([8, 2])
X = np.vstack((cluster1, cluster2, cluster3))

# --- 2. K-Means Implementation from Scratch ---
def run_kmeans(X, k, max_iters=100):
    # Randomly initialize centroids by picking k data points
    np.random.seed(42)
    random_indices = np.random.choice(X.shape[0], size=k, replace=False)
    centroids = X[random_indices]
    
    history = []
    
    for i in range(max_iters):
        # Compute distances (Euclidean) from points to centroids
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        
        # Assign points to the closest centroid
        labels = np.argmin(distances, axis=1)
        
        # Calculate Within-Cluster Sum of Squares (WCSS)
        wcss = 0
        for j in range(k):
            cluster_points = X[labels == j]
            if len(cluster_points) > 0:
                wcss += np.sum((cluster_points - centroids[j])**2)
        
        # Save state for visualization
        history.append({
            'iteration': i + 1, 
            'centroids': centroids.copy(), 
            'labels': labels.copy(), 
            'wcss': wcss
        })
        
        # Update centroids to the mean of assigned points
        new_centroids = np.zeros((k, 2))
        for j in range(k):
            cluster_points = X[labels == j]
            if len(cluster_points) > 0:
                new_centroids[j] = np.mean(cluster_points, axis=0)
            else:
                new_centroids[j] = centroids[j] # Handle empty clusters
                
        # Check for convergence (if centroids stop moving)
        if np.allclose(centroids, new_centroids):
            break
            
        centroids = new_centroids
        
    return history

# --- 3. Execution & Step-by-Step Visualization (K=3) ---
history_k3 = run_kmeans(X, k=3)

print("--- WCSS per Iteration (K=3) ---")
wcss_values = []
iterations = []
for step in history_k3:
    print(f"Iteration {step['iteration']}: WCSS = {step['wcss']:.2f}")
    wcss_values.append(step['wcss'])
    iterations.append(step['iteration'])
print("Converged!\n")

# Figure 1: Clustering Process (4 Subplots)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

# Prepare states to plot (safeguard in case it converges before iter 3)
plot_steps = [
    ("Initial Data", None), 
    ("Iteration 1", history_k3[0]), 
    ("Iteration 3", history_k3[2] if len(history_k3) > 2 else history_k3[-1]), 
    (f"Final Converged (Iter {history_k3[-1]['iteration']})", history_k3[-1])
]

colors = ['r', 'g', 'b']

for i, (title, step_data) in enumerate(plot_steps):
    ax = axes[i]
    if step_data is None:
        ax.scatter(X[:, 0], X[:, 1], c='gray', alpha=0.6)
    else:
        labels = step_data['labels']
        centroids = step_data['centroids']
        for j in range(3):
            cluster_points = X[labels == j]
            ax.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[j], alpha=0.6, label=f'Cluster {j+1}')
        ax.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='X', s=200, label='Centroids')
        
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# Figure 2: WCSS vs Iteration
plt.figure(figsize=(8, 5))
plt.plot(iterations, wcss_values, marker='o', linestyle='-', color='purple')
plt.title('WCSS vs. Iteration Number (K=3)')
plt.xlabel('Iteration')
plt.ylabel('WCSS')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# --- 4. Elbow Method (K=2 to 5) ---
k_values = [2, 3, 4, 5]
final_wcss = []

for k in k_values:
    hist = run_kmeans(X, k=k)
    final_wcss.append(hist[-1]['wcss'])

# Figure 3: Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(k_values, final_wcss, marker='s', linestyle='-', color='teal', markersize=8)
plt.title('Elbow Curve (WCSS vs. K)')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Final Converged WCSS')
plt.xticks(k_values)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()