import numpy as np
import pandas as pd
import random

# ------------------------------------
# DATASET CREATION: Breakups Dataset
# ------------------------------------

np.random.seed(42)
random.seed(42)

n = 2000  # 2,000 data points

data = {
    'Relationship_Duration_Years': np.random.exponential(scale=2.5, size=n).round(1),  # average ~2.5 years
    'Age_At_Breakup': np.random.normal(loc=25, scale=5, size=n).round(1),  # avg breakup age ~25 years
    'Number_of_Relationships': np.random.poisson(lam=3, size=n),  # avg ~3 relationships
    'Time_to_Move_On_Months': np.random.normal(loc=6, scale=2, size=n).clip(min=0).round(1),  # avg move-on ~6 months
    'Initiator': random.choices(['Self', 'Partner'], k=n)  # who initiated the breakup
}

df = pd.DataFrame(data)

# Save dataset to a CSV file
df.to_csv("breakups_dataset.csv", index=False)

print("Dataset created and saved as 'breakups_dataset.csv'.")
