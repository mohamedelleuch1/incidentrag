"""
test_chromadb_fake_data.py

Objectif (Person B, Jour 2) :
Apprendre à utiliser ChromaDB avec un petit jeu de données FACTICE,
sans attendre que Person A ait fini d'indexer les vraies 150 issues.

Qu'est-ce qu'une "collection" dans ChromaDB ?
Une collection est l'équivalent d'une "table" dans une base de données
classique : un espace nommé où on stocke des documents, chacun accompagné
de son embedding (sa représentation numérique) et de métadonnées (des
informations annexes, comme l'URL ou l'ID de l'issue d'origine).
"""

import chromadb
from chromadb.utils import embedding_functions

# --- ETAPE 1 : créer un "client" ChromaDB ---
# PersistentClient sauvegarde les données sur le disque (dans le dossier
# indiqué), pour qu'elles ne disparaissent pas à chaque redémarrage du script.
client = chromadb.PersistentClient(path="./chroma_test_db")

# --- ETAPE 2 : choisir la fonction d'embedding ---
# C'est elle qui transforme un texte en liste de nombres (le "vecteur").
# "all-MiniLM-L6-v2" est un modèle léger, gratuit, et qui tourne en local
# (pas besoin de clé API OpenAI).
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# --- ETAPE 3 : créer (ou récupérer) une collection ---
# get_or_create_collection évite une erreur si la collection existe déjà
# (utile quand on relance le script plusieurs fois pendant les tests).
collection = client.get_or_create_collection(
    name="fake_incidents",
    embedding_function=embedding_fn
)

# --- ETAPE 4 : données FACTICES (à remplacer par les vraies de Person A) ---
fake_incidents = [
    {
        "id": "fake_1",
        "title": "Pod Kubernetes redémarre en boucle",
        "body": "Après un déploiement, mon pod crash et redémarre sans arrêt.",
        "resolution": "Le readinessProbe était mal configuré, augmenter le délai initial l'a résolu.",
    },
    {
        "id": "fake_2",
        "title": "Connexion refusée sur le broker MQTT",
        "body": "Impossible de se connecter au broker, erreur connection refused.",
        "resolution": "Le firewall bloquait le port 1883, il fallait l'ouvrir.",
    },
    {
        "id": "fake_3",
        "title": "Fuite mémoire après plusieurs jours",
        "body": "Le process utilise de plus en plus de RAM avec le temps.",
        "resolution": "Un bug dans la gestion des connexions non fermées, corrigé dans la version suivante.",
    },
]


def index_fake_data():
    """
    Ajoute les incidents factices dans la collection ChromaDB.
    """
    # ChromaDB attend des listes séparées : les textes, les métadonnées, les ID
    documents = [f"{inc['title']}. {inc['body']}. {inc['resolution']}" for inc in fake_incidents]
    metadatas = [{"title": inc["title"], "resolution": inc["resolution"]} for inc in fake_incidents]
    ids = [inc["id"] for inc in fake_incidents]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ {len(fake_incidents)} incidents factices indexés dans ChromaDB.")


def search_incidents(query: str, n_results: int = 2):
    """
    LA fonction clé de ton rôle aujourd'hui.
    Prend une question en texte libre, et retourne les incidents
    les plus proches en SENS (pas juste en mots-clés).
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results


if __name__ == "__main__":
    # On indexe les données factices une seule fois
    if collection.count() == 0:
        index_fake_data()
    else:
        print(f"ℹ️ Collection déjà remplie ({collection.count()} documents), pas de ré-indexation.")

    # On teste une recherche
    test_query = "Mon serveur MQTT n'accepte pas les connexions"
    print(f"\n🔍 Recherche pour : '{test_query}'\n")

    results = search_incidents(test_query, n_results=2)

    for i, (doc, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"--- Résultat {i+1} (distance: {distance:.3f}) ---")
        print(f"Titre : {metadata['title']}")
        print(f"Résolution : {metadata['resolution']}\n")
