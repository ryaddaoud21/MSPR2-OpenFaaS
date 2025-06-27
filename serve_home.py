import requests
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__, static_folder='frontend')

# URL de base du gateway OpenFaaS
OPENFAAS_GATEWAY_URL = "http://34.38.245.109:8080/function"

@app.route('/')
def serve_home():
    # Page d'accueil, tu peux rediriger vers signup ou index.html
    return send_from_directory(app.static_folder, 'signup.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    # Sert tous les fichiers statiques (HTML, CSS, JS, images, etc.)
    return send_from_directory(app.static_folder, filename)

@app.route('/f/<function_name>', methods=['POST'])
def proxy_function_call(function_name):
    # Reçoit le JSON et le retransmet à la fonction OpenFaaS correspondante
    payload = request.get_json(force=True)
    url = f"{OPENFAAS_GATEWAY_URL}/{function_name}"
    try:
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        try:
            return jsonify(resp.json())
        except ValueError:
            # Si la réponse n’est pas JSON, renvoie brut
            return resp.text, resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erreur lors de l’appel OpenFaaS: {str(e)}"}), 500

if __name__ == '__main__':
    # Démarre le serveur Flask en mode debug
    app.run(debug=True, host='0.0.0.0', port=5000)
