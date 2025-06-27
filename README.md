
# 📘 HOWTO – Déploiement d’OpenFaaS sur Google Cloud GKE Autopilot (Windows)

## 🎯 Objectif :
Déployer OpenFaaS dans un cluster Kubernetes cloud (GKE Autopilot) à l’aide de :
- Google Cloud Platform (offre gratuite 300 $)
- helm (gestionnaire de charts Kubernetes)
- kubectl (client Kubernetes)
- faas-cli (client OpenFaaS)
- PowerShell / CMD sous Windows

## 🧰 Prérequis installés :
| Outil | Version | Installation |
|-------|---------|--------------|
| Google Cloud SDK | Dernière | https://cloud.google.com/sdk/docs/install |
| Helm | 3.18+ | `choco install kubernetes-helm` ou .zip |
| Kubectl | 1.33+ | `choco install kubernetes-cli` |
| faas-cli | 0.17+ | Via GitHub Releases |
| Docker (optionnel) | Dernière | Pour tests locaux avec Minikube |

## 🛠️ Étapes de déploiement sur GKE Autopilot :
### ✅ 1. Créer un cluster Kubernetes Autopilot
```bash
gcloud container clusters create-auto openfaas-cluster --region europe-west1
```

### ✅ 2. Se connecter au cluster
```bash
gcloud container clusters get-credentials openfaas-cluster --region europe-west1
```

### ✅ 3. Ajouter le repo Helm OpenFaaS
```bash
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update
```

### ✅ 4. Créer les namespaces
```bash
kubectl create namespace openfaas
kubectl create namespace openfaas-fn
```

### ✅ 5. Créer le secret admin
```bash
echo -n "admin" > user
echo -n "motdepasse" > password

kubectl -n openfaas create secret generic basic-auth   --from-file=basic-auth-user=user   --from-file=basic-auth-password=password
```

### ✅ 6. Installer OpenFaaS avec Helm
```bash
helm upgrade openfaas openfaas/openfaas `
  --install `
  --namespace openfaas `
  --set functionNamespace=openfaas-fn `
  --set generateBasicAuth=false `
  --set basic_auth=true `
  --set gateway.upstreamTimeout=60s
```

### ✅ 7. Exposer la Gateway via LoadBalancer
```cmd
kubectl patch svc gateway -n openfaas -p "{"spec": {"type": "LoadBalancer"}}"
```

### ✅ 8. Récupérer l’IP publique
```bash
kubectl get svc -n openfaas gateway
```

### ✅ 9. Récupérer le mot de passe admin
```bash
kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 -d
```

### ✅ 10. Connexion via faas-cli
```bash
faas-cli login --gateway http://[EXTERNAL-IP]:8080 --username admin --password [TON_MDP]
```

---

## ✅ Résultat obtenu :
- OpenFaaS déployé avec accès public via LoadBalancer
- Interface Web : `http://[EXTERNAL-IP]:8080`
- faas-cli fonctionnel

## 📦 Récapitulatif Projet MSPR avec OpenFaaS et Kubernetes

### 1. Architecture & Fonctionnalités
- OpenFaaS + Kubernetes GKE
- PostgreSQL
- Fonctions Python : `create-account-secure`, `authentication`, `generate-password`, `generate-2fa`, `verify-2fa`

### 2. Déploiement Kubernetes & OpenFaaS
- Cluster Autopilot GKE (e2-medium)
- OpenFaaS via Helm + LoadBalancer
- PostgreSQL dans namespace `openfaas-fn`
- Fonctions déployées via `faas-cli`

### 3. Proxy Flask pour Frontend
- Frontend en Flask + Bootstrap
- Proxy vers fonctions OpenFaaS (`/f/<function>`)

### 4. Frontend HTML/CSS/JS
- Pages : signup, login, dashboard, reset-password, 2FA
- JS centralisé dans app.js

### 5. Sécurité
- bcrypt pour mot de passe
- pyotp pour 2FA TOTP
- Validation côté serveur
- Communication API sécurisée

### 6. Déploiement & CI/CD
- faas-cli pour build/push/deploy
- Docker pour frontend Flask
- Kubernetes YAML pour proxy
- Automatisable avec script ou GitHub Actions

### 7. Améliorations possibles
- HTTPS + JWT
- Session utilisateur
- Déploiement frontend séparé
- Monitoring

### 8. PostgreSQL
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  password VARCHAR(255),
  mfa VARCHAR(255),
  gendate BIGINT,
  expired BOOLEAN
);
```

---

## 🧾 Déploiement d’un Frontend Flask avec Proxy vers OpenFaaS

### 📁 Structure du dossier
```
proxy-flask/
├── app.py
├── Dockerfile
├── requirements.txt
├── frontend/
│   ├── signup.html
│   ├── login.html
│   └── static/
│       ├── app.js
│       └── style.css
```

### 📄 Dockerfile
```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

### 📄 requirements.txt
```
Flask
requests
```

### 📄 app.py – Proxy vers OpenFaaS
```python
@app.route('/f/<function_name>', methods=['POST'])
def proxy_function_call(function_name):
    data = request.get_json(force=True)
    url = f"{OPENFAAS_GATEWAY_URL}/{function_name}"
    resp = requests.post(url, json=data)
    return jsonify(resp.json()), resp.status_code
```

### 🐳 Docker Build
```bash
docker build -t chtaybo22/mspr-proxy:latest .
docker push chtaybo22/mspr-proxy:latest
```

### ☁️ Déploiement Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mspr-proxy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mspr-proxy
  template:
    metadata:
      labels:
        app: mspr-proxy
    spec:
      containers:
      - name: proxy
        image: chtaybo22/mspr-proxy:latest
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: mspr-proxy-service
spec:
  type: LoadBalancer
  selector:
    app: mspr-proxy
  ports:
  - port: 80
    targetPort: 5000
```

### 🔧 Commandes utiles
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get svc mspr-proxy-service
```

### ✅ Résultat final
- Interface web servie via LoadBalancer GKE
- Appels API proxifiés vers OpenFaaS
- Système modulaire, sécurisé et scalable
