from flask import Flask, request, render_template,jsonify
import json
import webbrowser
import os
import requests
from uuid import uuid4
import random

app = Flask(__name__)

@app.route('/')
def index():	
    return render_template('index.html')

@app.route('/get_mind_map_data')
def get_mind_map_data(product_catalog=None):

	if product_catalog==None:
		product_catalog=generate_dummy_demo_data()

	mind_map_data = convert_to_jsmind_node_tree(product_catalog)
	return jsonify(mind_map_data)
	

@app.route('/getbook', methods=['GET'])
def getBookDataFromWeb():
	# Get the query parameter from the request
	query = request.args.get('q', '')  # Default to empty if no query provided
	
	if not query:
		return jsonify({"error": "Query parameter 'q' is required"}), 400

	# Make a request to the Google Books API
	url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
	
	try:
		response = requests.get(url)
		# If request is successful, parse the response as JSON
		if response.status_code == 200:
			data = response.json()['items']  # Get the JSON response
			root=query
			return creatMindMap(data,root)  # Return the data as JSON
		else:
			return jsonify({"error": "Failed to fetch data from Google Books API"}), response.status_code
	except requests.exceptions.RequestException as e:
		return jsonify({"error": str(e)}), 500


@app.route('/mindmap', methods=['POST'])
def mindmap():
	try:
		data = request.get_json()
		root=request.args.get('root', default='Home Listed')
		return creatMindMap(data,root)
		
	except Exception as e:
		return f"Error: {e}", 400

def creatMindMap(data,root):
	try:
		mind_data = convert_to_jsmind(data,root)
		htmlData=render_template('mindmap.html', mind_data=json.dumps(mind_data))
		
		file_path = os.path.abspath("output.html")
		with open(file_path, "w", encoding="utf-8") as f:
			f.write(htmlData)

		# Step 3: Open in browser
		webbrowser.open(f"file://{file_path}")
		return htmlData	
	except Exception as e:
		return f"Error: {e}", 400
		
def convert_to_jsmind(json_input,rootTopic):
	"""Convert nested dict/list into jsMind node_tree format."""
	root = {
		"id": "root",
		"topic": rootTopic,#"Root",
		"children": build_nodes("root", json_input)
	}

	return {
		"meta": { "name": "auto_mindmap", "author": "flask", "version": "1.0" },
		"format": "node_tree",
		"data": root
	}


def build_nodes(prefix, data):
	"""Recursive conversion of nested dicts/lists into jsMind nodes."""
	nodes = []

	if isinstance(data, dict):
		for key, value in data.items():
			node_id = f"{prefix}_{key}_{uuid4().hex[:6]}"
			if isinstance(value, (dict, list)):
				nodes.append({
					"id": node_id,
					"topic": str(key),
					"detail": json.dumps(value, indent=2),
					"children": build_nodes(node_id, value)
				})
			else:
				nodes.append({
					"id": node_id,
					"topic": f"{key}: {value}"
				})

	elif isinstance(data, list):
		for index, item in enumerate(data):	
			node_id = f"{prefix}_item{index}_{uuid4().hex[:6]}"
			nodes.append({
				"id": node_id,
				"topic": f"{item}",#f"Item {index}",
				"detail": f"{item} (expand to see details)",
				"children": build_nodes(node_id, item)
			})
			
	return nodes


# Generate nested data with 2 to 3 attributes per level, and 5 levels deep
def generate_nested_data(depth, base_key="level"):
	current_level = {}
	num_attrs = random.randint(2, 3)
	for i in range(1, num_attrs + 1):
		current_level[f"{base_key}_attr{i}"] = f"value_{random.randint(100,999)}"

	if depth > 1:
		current_level[f"{base_key}_{depth}"] = generate_nested_data(depth - 1, base_key)

	return current_level

def generate_dummy_demo_data():
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
	return products

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

####################################### Dummy Demo Data ##################################################################

	
if __name__ == '__main__':
	app.run(debug=True)
