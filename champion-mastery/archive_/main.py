import json
import os

# Define the path to your JSON file
json_file_path = "champions.json"  # Change this to your actual file path

# Check if file exists
if not os.path.exists(json_file_path):
    print(f"Error: File '{json_file_path}' not found.")
    exit(1)

# Load JSON data
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract champion names
champion_names = list(data["data"].keys())

# Generate URLs for each champion
base_url = "https://ddragon.leagueoflegends.com/cdn/15.5.1/data/en_US/champion/"
champion_urls = [f"{base_url}{name}.json" for name in champion_names]

# Print results
print("Champion Names and URLs:")
for name, url in zip(champion_names, champion_urls):
    print(f"{name}: {url}")

# Optional: Save results to a file
output_file = "champion_urls.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for name, url in zip(champion_names, champion_urls):
        f.write(f"{name}: {url}\n")

print(f"\nChampion URLs have been saved to '{output_file}'.")
