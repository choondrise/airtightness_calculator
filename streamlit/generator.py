import pandas as pd
import numpy as np

def generate_co2_data():
    # Generate timestamps for 24 hours at minute intervals
    timestamps = pd.date_range(start='2023-01-01', periods=1440, freq='T')

    # Generate CO₂ levels with more fluctuations
    co2_levels = []
    base_level = 400  # Starting point for CO₂ level
    for i in range(len(timestamps)):
        # Create variations by adding random noise
        variation = np.random.normal(loc=0, scale=20)  # Normal distribution with mean 0 and std deviation 20
        new_level = base_level + variation
        new_level = max(200, min(600, new_level))  # Keep values between 200 and 600
        co2_levels.append(new_level)
        
        # Update base level for some variability
        if i % 60 == 0:  # Every hour, change the base level slightly
            base_level += np.random.randint(-5, 6)  # Change by -5 to 5

    # Create a DataFrame
    df = pd.DataFrame({'timestamp': timestamps, 'co2_level': co2_levels})
    
    # Save to CSV if needed
    df.to_csv('co2_data.csv', index=False)

    return df
