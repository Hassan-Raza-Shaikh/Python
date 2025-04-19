import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
num_samples = 1000
data = {
    'Crash_ID': range(1, num_samples + 1),
    'Severity': np.random.choice(['Minor', 'Moderate', 'Severe'], num_samples, p=[0.5, 0.3, 0.2]),
    'Weather_Condition': np.random.choice(['Clear', 'Rain', 'Snow', 'Fog'], num_samples),
    'Road_Condition': np.random.choice(['Dry', 'Wet', 'Icy'], num_samples),
    'Time_of_Day': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], num_samples),
    'Injury_Count': np.random.poisson(1, num_samples)  # Poisson distribution for injury count
}

# Create a DataFrame
car_crashes_df = pd.DataFrame(data)

# Save to CSV
car_crashes_df.to_csv('car_crashes.csv', index=False)

print("Synthetic car crash dataset created and saved as 'car_crashes.csv'.")