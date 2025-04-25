```markdown```
# Fullstack News App - Frontend

Ce projet correspond à la partie **frontend** de l'application **Fullstack News App**, développé avec **Next.js** et **Chakra UI**.

Il permet de gérer l'affichage des **actualités (news)**, avec une **page de connexion**, une **page de dashboard**, et des interactions via une **API FastAPI** côté backend.

## Prérequis

- **Node.js** (version recommandée : 18+)
- **npm** (ou **pnpm** si tu souhaites adapter)

## Installation

1. Place-toi dans le dossier **frontend** :

```bash```
cd next-js-project/nextjs-dashboard

2. Installe les dépendances npm :

```bash```
npm install

3. Copie le fichier .env.example vers .env.local :

```bash```
cp .env.example .env.local

4. Remplis les variables d’environnement dans .env.local :

POSTGRES_URL=
AUTH_SECRET=

## Note : Actuellement, le projet utilise une base SQLite locale (db.sqlite3.db) via better-sqlite3. Cette base n'est pas versionnée (elle est ignorée dans Git). Si besoin, tu peux créer une base vide ou utiliser un script d'initialisation.

Lancement de l'application
```bash```
npm run dev

L'application sera disponible sur :

http://localhost:3000

Fonctionnalités principales

Page de connexion sécurisée.
Affichage et gestion des news via un backend FastAPI.
Utilisation de Chakra UI pour le design et l'interface utilisateur.
Base locale SQLite pour des fonctionnalités internes côté frontend (optionnel).

Structure du projet

next-js-project/nextjs-dashboard
├── app/              # Pages et routes Next.js (App Router)
├── components/       # Composants réutilisables (LoginForm, etc.)
├── database/         # Fichier de connexion SQLite (better-sqlite3)
├── public/           # Fichiers publics (favicon, images)
├── .env.example      # Exemple de configuration des variables d'environnement
├── package.json      # Dépendances npm
└── README.md         # Documentation du projet