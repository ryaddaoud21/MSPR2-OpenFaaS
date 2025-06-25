from flask import Flask, request, jsonify
from .handler import handle

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    try:
        result = handle(request.get_data(as_text=True))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
