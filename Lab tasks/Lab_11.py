import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv('Mall_Customers.csv')

df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
df.drop('CustomerID', axis=1, inplace=True)
df_relevant = df[['Gender', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)']]

gender_counts = df['Gender'].value_counts()
plt.bar(['Male', 'Female'], gender_counts)
plt.title("Gender Count")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

plt.hist(df['Age'], bins=20, color='skyblue', edgecolor='black')
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

plt.scatter(df['Age'], df['Spending Score (1-100)'], color='purple')
plt.title("Age vs Spending Score")
plt.xlabel("Age")
plt.ylabel("Spending Score")
plt.show()

plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], color='green')
plt.title("Annual Income vs Spending Score")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score")
plt.show()

plt.boxplot([df[df['Gender'] == 0]['Spending Score (1-100)'], df[df['Gender'] == 1]['Spending Score (1-100)']], labels=['Male', 'Female'])
plt.title("Spending Score by Gender")
plt.ylabel("Spending Score")
plt.show()

X = df[['Annual Income (k$)', 'Spending Score (1-100)']]
kmeans = KMeans(n_clusters=3, random_state=0)
df['Cluster'] = kmeans.fit_predict(X)

print("Cluster counts:\n", df['Cluster'].value_counts())
print("Cluster Centers:\n", kmeans.cluster_centers_)

plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], c=df['Cluster'], cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='red', marker='X', s=200, label='Centroids')
plt.title("Customer Segments with Cluster Centers")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.legend()
plt.show()

print("Cluster Analysis: One cluster with high Annual Income and high Spending Score represents top customers.")
print("Insight: A different cluster represents customers with both low income and low spending.")

plt.scatter(df['Age'], df['Spending Score (1-100)'], c=df['Cluster'], cmap='viridis')
plt.title("Age vs Spending Score by Cluster")
plt.xlabel("Age")
plt.ylabel("Spending Score")
plt.legend()
plt.show()
