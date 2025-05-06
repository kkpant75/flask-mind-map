import json
import random

# Generate nested data with 2 to 3 attributes per level, and 5 levels deep
def generate_nested_data(depth, base_key="level"):
    current_level = {}
    num_attrs = random.randint(2, 3)
    for i in range(1, num_attrs + 1):
        current_level[f"{base_key}_attr{i}"] = f"value_{random.randint(100,999)}"

    if depth > 1:
        current_level[f"{base_key}_{depth}"] = generate_nested_data(depth - 1, base_key)

    return current_level

# Create 10 product entries
products = []
for i in range(10):
    product = {
        "id": f"P{1000+i}",
        "name": f"Product {i+1}",
        "category": random.choice(["Electronics", "Home Appliances", "Mobile Phones"]),
        "details": generate_nested_data(5)
    }
    products.append(product)

# Save to JSON file 


with open("inputjson.json", "w") as f:
    json.dump(products, f, indent=2)

print("inputjson.json has been created.")
