# MSPR2 - OpenFaaS Serverless Project

Ce projet met en œuvre plusieurs fonctions **serverless** avec [OpenFaaS](https://www.openfaas.com/) et une base de données **PostgreSQL** sur **Kubernetes**. Il simule un système sécurisé de gestion d'utilisateurs.

## 🚀 Fonctionnalités

| Fonction                 | Description |
|--------------------------|-------------|
| `create-account-secure` | Création sécurisée d’un compte utilisateur |
| `authentication`        | Authentification d’un utilisateur avec username + password |
| `generate-2fa`          | Génération d’un secret TOTP + QR Code pour MFA |
| `generate-password`     | Génération et mise à jour d’un mot de passe complexe |

---

## 🧱 Architecture

- **Backend Functions** : OpenFaaS Functions (Python)
- **Base de données** : PostgreSQL 15 (déployée dans Kubernetes)
- **Plateforme** : Kubernetes avec `faas-netes`

---


---


🧑‍💻 Auteur
Projet réalisé dans le cadre du MSPR2 à l’EPSI Toulouse
© 2025 - Ryad D.