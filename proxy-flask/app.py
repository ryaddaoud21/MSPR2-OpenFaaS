import requests
from flask import Flask, send_from_directory, request, jsonify, render_template

app = Flask(__name__, static_folder='frontend', static_url_path='')

# URL du gateway OpenFaaS
OPENFAAS_GATEWAY_URL = "http://34.38.245.109:8080/function"

@app.route('/')
def serve_signup():
    return send_from_directory(app.static_folder, 'signup.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/f/<function_name>', methods=['POST'])
def proxy_function_call(function_name):
    try:
        data = request.get_json(force=True)
        url = f"{OPENFAAS_GATEWAY_URL}/{function_name}"
        resp = requests.post(url, json=data)

        # Essayons de renvoyer JSON, sinon texte
        try:
            return jsonify(resp.json()), resp.status_code
        except ValueError:
            return resp.text, resp.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
