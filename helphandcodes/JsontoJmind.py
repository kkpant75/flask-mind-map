
def convert_to_jsmind_node_tree(products):
    root = {
        "id": "root",
        "topic": "Product Catalog",
        "children": []
    }

    def build_children(prefix, data):
        nodes = []
        if isinstance(data, dict):
            for k, v in data.items():
                node_id = f"{prefix}_{k}"
                if isinstance(v, (dict, list)):
                    child = {
                        "id": node_id,
                        "topic": k.capitalize(),
                        "children": build_children(node_id, v)
                    }
                else:
                    child = {
                        "id": node_id,
                        "topic": f"{k.capitalize()}: {v}"
                    }
                nodes.append(child)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                node_id = f"{prefix}_{idx}"
                child = {
                    "id": node_id,
                    "topic": f"Item {idx + 1}",
                    "children": build_children(node_id, item)
                }
                nodes.append(child)
        return nodes

    for product in products:
        product_node = {
            "id": product["id"],
            "topic": product["name"],
            "children": build_children(product["id"], {
                "category": product["category"],
                "details": product["details"]
            })
        }
        root["children"].append(product_node)

    return {
        "meta": {
            "name": "product_catalog",
            "author": "ChatGPT",
            "version": "1.0"
        },
        "format": "node_tree",
        "data": root
    }

import json
with open('inputjson.json', 'r') as f:
    product_catalog = json.load(f)

jsmind_data = convert_to_jsmind_node_tree(product_catalog)

print(json.dumps(jsmind_data, indent=2))

open("jmind.json","w").write(json.dumps(jsmind_data, indent=2))