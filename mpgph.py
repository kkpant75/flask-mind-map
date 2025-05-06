import json
from graphviz import Digraph

# Sample product catalog JSON (can be loaded from a file as well)
product_catalog = [
    {
        "id": "P1001",
        "name": "Laptop Pro 15",
        "category": "Electronics",
        "details": {
            "brand": "TechMaster",
            "specs": {
                "processor": "Intel Core i7",
                "ram": "16GB",
                "storage": {
                    "type": "SSD",
                    "capacity": "512GB"
                },
                "display": {
                    "size": "15.6 inch",
                    "resolution": "1920x1080"
                }
            },
            "warranty": {
                "period": "2 years",
                "type": "Onsite"
            }
        }
    },
    {
        "id": "P2002",
        "name": "Smartphone Max X",
        "category": "Mobile Phones",
        "details": {
            "brand": "PhoneZone",
            "specs": {
                "os": "Android 13",
                "camera": {
                    "rear": "108MP",
                    "front": "32MP"
                },
                "battery": {
                    "capacity": "5000mAh",
                    "type": "Li-ion"
                },
                "network": {
                    "5G": True,
                    "eSIM": True
                }
            },
            "warranty": {
                "period": "1 year",
                "type": "Carry-in"
            }
        }
    },
    {
        "id": "P3003",
        "name": "SmartCool Fridge 300L",
        "category": "Home Appliances",
        "details": {
            "brand": "CoolTech",
            "specs": {
                "capacity": "300L",
                "energy_rating": "4 Star",
                "features": {
                    "convertible": True,
                    "inverter": True,
                    "smart_control": False
                },
                "dimensions": {
                    "height": "170cm",
                    "width": "60cm",
                    "depth": "68cm"
                }
            },
            "warranty": {
                "period": "10 years",
                "type": "Compressor only"
            }
        }
    }
]

# Initialize graph
dot = Digraph(format='png')
dot.attr(rankdir='LR')  # Left to Right layout

# Recursive function to add nodes and edges
def add_subtree(parent_id, tree):
    if isinstance(tree, dict):
        for key, value in tree.items():
            node_id = f"{parent_id}.{key}"
            label = key if isinstance(value, (dict, list)) else f"{key}: {value}"
            dot.node(node_id, label)
            dot.edge(parent_id, node_id)
            add_subtree(node_id, value)
    elif isinstance(tree, list):
        for idx, item in enumerate(tree):
            node_id = f"{parent_id}[{idx}]"
            label = f"Item {idx + 1}"
            dot.node(node_id, label)
            dot.edge(parent_id, node_id)
            add_subtree(node_id, item)
    else:
        # Leaf node
        leaf_id = f"{parent_id}_leaf"
        dot.node(leaf_id, str(tree))
        dot.edge(parent_id, leaf_id)

# Add each product as a root and build tree
for idx, product in enumerate(product_catalog):
    root_label = f"{product['name']} ({product['id']})"
    root_id = f"Product{idx}"
    dot.node(root_id, root_label)
    add_subtree(root_id, product)

# Render and view mind map
dot.render('product_catalog_mindmap', view=True)
