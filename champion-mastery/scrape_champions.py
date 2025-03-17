import requests
import os

# Define the input file
input_file = "champion_urls.txt"
output_folder = "champion_data"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Read the champion URLs from the file
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Process each line
for line in lines:
    if not line.strip():
        continue  # Skip empty lines

    try:
        # Extract champion name and URL
        champion_name, url = line.split(": ")
        champion_name = champion_name.strip()
        url = url.strip()

        print(f"Fetching data for {champion_name}...")

        # Fetch data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Save the JSON data to a file
        output_file = os.path.join(output_folder, f"{champion_name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Saved: {output_file}")

    except Exception as e:
        print(f"Error fetching {champion_name}: {e}")

print("\nAll champion data has been scraped and saved.")
