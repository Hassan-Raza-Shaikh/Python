import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd

# Generate a date range
dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
x = np.linspace(0, 10, 100)
y1 = np.sin(x) + np.random.normal(0, 0.2, 100)
y2 = np.cos(x) * 50 + np.random.normal(0, 5, 100)

# Complex figure setup
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Complex Multi-Panel Matplotlib Graph", fontsize=16)

# --- Plot 1: Time Series Line Plot with Twin Axis ---
ax1 = axs[0, 0]
ax1.plot(dates, y1, color='tab:blue', label='Sine + Noise')
ax1.set_ylabel("Sine Value", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax1b = ax1.twinx()
ax1b.plot(dates, y2, color='tab:red', label='Cosine * 50 + Noise')
ax1b.set_ylabel("Cosine * 50", color='tab:red')
ax1b.tick_params(axis='y', labelcolor='tab:red')
ax1.set_title("Dual Axis Time Series")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.grid(True)

# --- Plot 2: Scatter Plot with Gradient Coloring ---
ax2 = axs[0, 1]
colors = np.sqrt(x**2 + y1**2)
scatter = ax2.scatter(x, y1, c=colors, cmap='viridis', s=60, edgecolor='k')
fig.colorbar(scatter, ax=ax2, label='Color Scale (sqrt(x² + y²))')
ax2.set_title("Gradient Colored Scatter Plot")
ax2.set_xlabel("X Value")
ax2.set_ylabel("Y Value")

# --- Plot 3: Histogram with Multiple Series ---
ax3 = axs[1, 0]
data_a = np.random.normal(0, 1, 1000)
data_b = np.random.normal(1, 1.5, 1000)
ax3.hist(data_a, bins=30, alpha=0.6, label='Normal (0,1)', color='blue')
ax3.hist(data_b, bins=30, alpha=0.6, label='Normal (1,1.5)', color='orange')
ax3.legend()
ax3.set_title("Overlapping Histograms")
ax3.set_xlabel("Value")
ax3.set_ylabel("Frequency")

# --- Plot 4: Heatmap ---
ax4 = axs[1, 1]
heat_data = np.random.rand(10, 10)
cax = ax4.imshow(heat_data, cmap='coolwarm', interpolation='nearest')
fig.colorbar(cax, ax=ax4, orientation='vertical', label='Heat Intensity')
ax4.set_title("Random Heatmap")
ax4.set_xticks(np.arange(10))
ax4.set_yticks(np.arange(10))

# Layout adjustment
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()