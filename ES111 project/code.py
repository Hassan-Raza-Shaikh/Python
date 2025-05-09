import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load your dataset
df = pd.read_csv("Spotify_final_dataset.csv")

# Clean column names (remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# Convert relevant columns to numeric, removing non-numeric parts
df['Top 10 Times'] = df['Top 10 (xTimes)'].str.replace('(x', '', regex=False).str.replace(')', '', regex=False).astype(float)
df['Peak Position Times'] = df['Peak Position (xTimes)'].str.replace('(x', '', regex=False).str.replace(')', '', regex=False).astype(float)

# Convert other numeric columns
df['Days'] = df['Days'].astype(int)
df['Peak Position'] = df['Peak Position'].astype(int)
df['Peak Streams'] = df['Peak Streams'].astype(int)
df['Total Streams'] = df['Total Streams'].astype(int)

# Describe basic stats
print(df[['Days', 'Top 10 Times', 'Peak Position', 'Peak Position Times', 'Peak Streams', 'Total Streams']].describe())

# Histogram of Total Streams
plt.figure(figsize=(10, 6))
sns.histplot(df['Total Streams'], bins=30, kde=True)
plt.title('Distribution of Total Streams')
plt.xlabel('Total Streams')
plt.ylabel('Frequency')
plt.show()

# Pie chart: top 5 artists by number of entries
top_artists = df['Artist Name'].value_counts().head(5)
plt.figure(figsize=(8, 8))
top_artists.plot.pie(autopct='%1.1f%%')
plt.title('Top 5 Artists by Number of Songs in Dataset')
plt.ylabel('')
plt.show()

# Frequency distribution of Peak Position
peak_position_bins = [1, 5, 10, 20, 50, 100]
df['Peak Pos Bin'] = pd.cut(df['Peak Position'], bins=peak_position_bins)
freq_distribution = df['Peak Pos Bin'].value_counts().sort_index()
print("\nFrequency Distribution of Peak Positions:")
print(freq_distribution)

# Mean & variance of Total Streams
mean_streams = df['Total Streams'].mean()
var_streams = df['Total Streams'].var()
print(f"\nMean of Total Streams: {mean_streams}")
print(f"Variance of Total Streams: {var_streams}")

# Confidence interval (95%) for Total Streams using 80% of data
sample = df.sample(frac=0.8, random_state=42)
remaining = df.drop(sample.index)

sample_mean = sample['Total Streams'].mean()
sample_se = stats.sem(sample['Total Streams'])
confidence_interval = stats.t.interval(0.95, len(sample)-1, loc=sample_mean, scale=sample_se)
print(f"\n95% Confidence Interval for Mean of Total Streams: {confidence_interval}")

# 95% tolerance interval (approximate, assuming normality)
z = stats.norm.ppf(0.975)
tolerance_interval = (sample_mean - z * np.std(sample['Total Streams'], ddof=1),
                      sample_mean + z * np.std(sample['Total Streams'], ddof=1))
print(f"95% Tolerance Interval for Total Streams: {tolerance_interval}")

# Validate with the remaining 20%
within_tolerance = remaining['Total Streams'].between(*tolerance_interval).mean()
print(f"\nPercentage of Remaining Data within Tolerance Interval: {within_tolerance * 100:.2f}%")

# Hypothesis: Songs in top 10 more often have more total streams
top_10_more = df[df['Top 10 Times'] > df['Top 10 Times'].median()]
top_10_less = df[df['Top 10 Times'] <= df['Top 10 Times'].median()]
t_stat, p_val = stats.ttest_ind(top_10_more['Total Streams'], top_10_less['Total Streams'], equal_var=False)
print(f"\nT-test: Does being in Top 10 more often mean higher streams?")
print(f"T-statistic: {t_stat}, P-value: {p_val}")

if p_val < 0.05:
    print("Result: Statistically significant difference.")
else:
    print("Result: No significant difference.")
