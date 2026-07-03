# IncidentRAG

Assistant RAG qui aide à diagnostiquer des bugs techniques en s'appuyant sur l'historique réel d'incidents résolus du repo GitHub [eclipse-mosquitto/mosquitto](https://github.com/eclipse-mosquitto/mosquitto).

## 🎯 Objectif du projet

Plutôt que de répondre à partir d'une connaissance générale, ce système retrouve des incidents similaires déjà résolus dans l'historique du projet Mosquitto (broker MQTT open source), et génère un diagnostic basé sur des cas réels et vérifiables.

## 📂 Structure du projet

## 📊 Le corpus de données

Le fichier `incidents_clean.json` contient environ 150 issues fermées du repo `eclipse-mosquitto/mosquitto`, sélectionnées pour maximiser la diversité :

- **60% triées par nombre de commentaires** → garantit des résolutions riches et bien documentées
- **40% triées par date de mise à jour** → garantit une couverture des problèmes récents

Chaque incident a le format suivant :

```json
{
  "id": 529,
  "title": "Titre de l'issue",
  "body": "Description complète du problème",
  "url": "https://github.com/eclipse-mosquitto/mosquitto/issues/529",
  "closed_at": "2018-04-10T10:30:16Z",
  "comments_count": 82,
  "source_sort": "comments",
  "resolution": "Le commentaire de résolution le plus substantiel"
}
```

## 🛠️ Stack technique (extraction)

- **Python 3.10+**
- `requests` — appels à l'API GitHub REST
- `python-dotenv` — gestion du token GitHub en variable d'environnement

## ⚙️ Comment relancer l'extraction

### 1. Créer un token GitHub
Sur `github.com/settings/tokens`, générer un token classique avec le scope `public_repo`.

### 2. Configurer l'environnement
Créer un fichier `.env` à la racine (non versionné, protégé par `.gitignore`) :

### 3. Installer les dépendances
```bash
pip install requests python-dotenv
```

### 4. Lancer l'extraction
```bash
python test_extraction.py
```

Le script génère `incidents_clean.json` avec ~150 incidents diversifiés.

## 🚀 Prochaines étapes du projet

- [ ] Chunking et indexation vectorielle (embeddings + ChromaDB)
- [ ] Pipeline de retrieval (recherche des incidents similaires)
- [ ] Génération du diagnostic (LLM + prompt structuré)
- [ ] Interface Streamlit

## 👥 Équipe

- **Personne A** — Collecte de données, pipeline d'extraction
- **Personne B** — Indexation, retrieval, génération, interface