import matplotlib.pyplot as plt

# Categories
categories = ['Objectives', 'Technologies', 'Outcomes']

# Weighted data (values from 0–10 showing contribution intensity)
data = {
    'Resume Screening': [9, 0, 0],
    'AI Interviews': [10, 0, 0],
    'Bias Mitigation': [8, 0, 0],
    'ATS Integration': [7, 0, 0],

    'NLP': [0, 9, 0],
    'Deep Learning': [0, 8, 0],
    'Deepfake Avatars': [0, 10, 0],
    'React + Flask': [0, 7, 0],

    '90% Parsing Accuracy': [0, 0, 8],
    '95% Uptime': [0, 0, 7],
    'Time Saved': [0, 0, 9],
    'Fairness Boost': [0, 0, 10]
}

labels = list(data.keys())
values = list(data.values())
stacked_values = list(zip(*values))

bar_width = 0.6
fig, ax = plt.subplots(figsize=(12, 7))

bottom = [0] * len(labels)
colors = ['lightblue', 'lightgreen', 'salmon']

# Plot each category as a stacked bar
for i, (cat, color) in enumerate(zip(categories, colors)):
    heights = stacked_values[i]
    ax.bar(labels, heights, bar_width, bottom=bottom, label=cat, color=color)
    bottom = [sum(x) for x in zip(bottom, heights)]

# Style
plt.xticks(rotation=75, ha='right', fontsize=9)
plt.ylabel('Contribution Level (0–10)')
plt.title('HiRay Project Summary: Weighted Contributions by Category')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
