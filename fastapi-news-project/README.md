# Fullstack News App - Backend

Ce projet correspond à la partie **backend** de l'application **Fullstack News App**, développé avec **FastAPI** et **SQLModel**.

Il fournit les **API REST** permettant de gérer les **actualités (news)** et les **catégories**, avec une authentification par **API Key** et des scopes d'accès.

## Prérequis

- **Python 3.10+**
- **pipenv** (gestionnaire d'environnements virtuels)

## Installation

1. Clone le projet et place-toi dans le dossier **backend** :

```bash```
cd fullstack-news-app/backend

2. Installe les dépendances avec pipenv :

```bash```
pipenv install --dev

3. Active l'environnement virtuel :

```bash```
pipenv shell

4. Assure-toi d'avoir un fichier .env à la racine avec les variables nécessaires (par exemple la connexion PostgreSQL si utilisée).

## Note :
 Le projet utilise SQLModel avec PostgreSQL (ou SQLite pour les tests). La base de données est non versionnée (fichier .env ignoré dans Git).

## Lancement du serveur

```bash```
uvicorn app.main:app --reload

Le serveur sera disponible sur :

http://localhost:8000

## Lancement des tests

Pour lancer les tests d'intégration avec pytest :

```bash```
pytest

## Fonctionnalités principales

API REST pour gérer les news et catégories.
Authentification API Key avec gestion des scopes (droits d'accès).
SQLModel pour la gestion de la base de données.
Tests d'intégration end-to-end avec pytest.

## Structure du projet

backend
├── app/                 # Code principal de l'application FastAPI
│   ├── main.py          # Point d'entrée FastAPI
│   └── ...              # Autres fichiers (routes, modèles, etc.)
├── scripts/             # Scripts utilitaires (ex: init DB)
├── tests/               # Tests d'intégration Pytest
├── .env                 # Variables d'environnement (non versionné)
├── Pipfile              # Dépendances pipenv
├── Pipfile.lock         # Verrouillage des versions des dépendances
└── README.md            # Documentation du projet backend
