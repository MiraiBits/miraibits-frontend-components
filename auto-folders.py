import os
import json

# Path to your JSON file
json_file = "products.json"

# Path to the base folder
base_folder = "products"

# Make sure the base folder exists
if not os.path.exists(base_folder):
    print(f"Error: Base folder '{base_folder}' does not exist.")
    exit(1)

# Load the JSON data
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Go through each product
for product in data.get("products", []):
    slug = product.get("slug")
    if not slug:
        print("Skipping product without slug.")
        continue

    # Create folder path
    folder_path = os.path.join(base_folder, slug)

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    print(f"Created folder: {folder_path}")

print("✅ All product folders have been created successfully!")
