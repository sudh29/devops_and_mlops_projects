import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask inside Container!",
        "status": "online"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-sample"
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
