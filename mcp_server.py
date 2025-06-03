from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/handshake", methods=["POST"])
def handshake():
    return jsonify({"capabilities": ["read_file"], "protocol_version": "1.0"})

@app.route("/request", methods=["POST"])
def handle_request():
    data = request.json
    if data.get("action") == "read_file":
        # Simulate reading a file
        return jsonify({"success": True, "data": "Sample file contents"})
    return jsonify({"success": False, "error": "Unknown action"})

if __name__ == "__main__":
    app.run(port=8000)