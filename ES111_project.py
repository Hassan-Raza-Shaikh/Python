import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# ------------------------------------
# LOAD BREAKUPS DATASET
# ------------------------------------
df = pd.read_csv("breakups_dataset.csv")

# ------------------------------------
# 1. AVERAGE AND VARIANCE (Direct Calculation)
# ------------------------------------
mean_duration = df['Relationship_Duration_Years'].mean()
var_duration = df['Relationship_Duration_Years'].var()

print(f"Mean Relationship Duration: {mean_duration:.2f} years")
print(f"Variance of Relationship Duration: {var_duration:.2f}")

# ------------------------------------
# 2. HISTOGRAM, PIE CHART, FREQUENCY DISTRIBUTION
# ------------------------------------
# Histogram of Relationship Duration
plt.figure(figsize=(8,5))
plt.hist(df['Relationship_Duration_Years'], bins=20, color='skyblue', edgecolor='black')
plt.title('Histogram of Relationship Duration')
plt.xlabel('Years')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Pie chart for Initiator
initiator_counts = df['Initiator'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(initiator_counts, labels=initiator_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
plt.title('Who Initiated the Breakup')
plt.show()

# Frequency distribution (grouped)
bins = [0, 1, 2, 3, 5, 10, 20]
labels = ['<1', '1-2', '2-3', '3-5', '5-10', '10+']
df['Duration_Group'] = pd.cut(df['Relationship_Duration_Years'], bins=bins, labels=labels, right=False)
frequency_distribution = df['Duration_Group'].value_counts().sort_index()

print("\nFrequency Distribution:")
print(frequency_distribution)

# ------------------------------------
# 3. AVERAGE AND VARIANCE (From Frequency Distribution)
# ------------------------------------
# Midpoints for each group
midpoints = {
    '<1': 0.5,
    '1-2': 1.5,
    '2-3': 2.5,
    '3-5': 4,
    '5-10': 7.5,
    '10+': 15
}

freq_df = pd.DataFrame({
    'Midpoint': [midpoints[label] for label in labels],
    'Frequency': frequency_distribution.values
})

mean_fd = (freq_df['Midpoint'] * freq_df['Frequency']).sum() / freq_df['Frequency'].sum()
var_fd = (((freq_df['Midpoint'] - mean_fd)**2 * freq_df['Frequency']).sum()) / (freq_df['Frequency'].sum() - 1)

print(f"\nMean (from Frequency Distribution): {mean_fd:.2f} years")
print(f"Variance (from Frequency Distribution): {var_fd:.2f}")

# Comparison
print("\nComparison:")
print(f"Difference in Mean: {abs(mean_duration - mean_fd):.4f}")
print(f"Difference in Variance: {abs(var_duration - var_fd):.4f}")

# ------------------------------------
# 4. CONFIDENCE AND TOLERANCE INTERVALS
# ------------------------------------
# Split data: 80% sample, 20% validation
sample_df = df.sample(frac=0.8, random_state=1)
validation_df = df.drop(sample_df.index)

sample_mean = sample_df['Relationship_Duration_Years'].mean()
sample_std = sample_df['Relationship_Duration_Years'].std()
sample_size = len(sample_df)

# 95% Confidence Interval for Mean
conf_level = 0.95
z_score = stats.norm.ppf(1 - (1-conf_level)/2)
margin_error = z_score * (sample_std / np.sqrt(sample_size))
conf_interval = (sample_mean - margin_error, sample_mean + margin_error)

print(f"\n95% Confidence Interval for Mean: {conf_interval}")

# 95% Tolerance Interval
k_factor = stats.t.ppf(conf_level, df=sample_size-1) * np.sqrt(1 + 1/sample_size)
tol_interval = (sample_mean - k_factor * sample_std, sample_mean + k_factor * sample_std)

print(f"95% Tolerance Interval: {tol_interval}")

# Validation
within_interval = ((validation_df['Relationship_Duration_Years'] >= tol_interval[0]) & 
                   (validation_df['Relationship_Duration_Years'] <= tol_interval[1])).mean()

print(f"Proportion of Validation Data within Tolerance Interval: {within_interval*100:.2f}%")

# ------------------------------------
# 5. HYPOTHESIS TESTING
# Hypothesis: People in longer relationships take longer to move on
# ------------------------------------
long_relationships = df[df['Relationship_Duration_Years'] > 3]['Time_to_Move_On_Months']
short_relationships = df[df['Relationship_Duration_Years'] <= 3]['Time_to_Move_On_Months']

# Two-sample t-test
t_stat, p_value = stats.ttest_ind(long_relationships, short_relationships, equal_var=False)

print("\nHypothesis Testing:")
print(f"t-statistic: {t_stat:.2f}, p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Conclusion: Statistically significant difference. Longer relationships take longer to move on.")
else:
    print("Conclusion: No significant difference found.")
