import requests
import pandas as pd
import os

# Set location 
latitude = -26.2041  # Johannesburg
longitude = 28.0473
location_name = "johannesburg"

# Date range (1 full year)
start_date = "2023-01-01"
end_date = "2023-12-31"

# API URL
url = (
    f"https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    f"&timezone=Africa%2FJohannesburg"
)

# Request + Parse
response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data["daily"])

# Ensure data/processed exists
os.makedirs("data/processed", exist_ok=True)

# Save CSV
output_path = f"data/processed/{location_name}_2023_weather.csv"
df.to_csv(output_path, index=False)
print(f"✅ Weather data saved to {output_path}")
