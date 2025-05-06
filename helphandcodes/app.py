from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
	
@app.route("/")
def index():
    return render_template("mindmap.html")

@app.route("/node_click", methods=["POST"])
def node_click():
    data = request.get_json()
    print("Node clicked:", data)  # See this in the terminal
    return jsonify({"status": "OK", "received": data})

if __name__ == "__main__":
    app.run(debug=True)
