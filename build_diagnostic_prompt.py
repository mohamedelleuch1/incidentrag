"""
build_diagnostic_prompt.py

Objectif (Person B, Jour 2) :
Préparer la structure du prompt de diagnostic, AVANT d'avoir les vrais
résultats de recherche de ChromaDB. On utilise des résultats FACTICES,
codés en dur, pour tester la construction du prompt dès maintenant.
"""

# --- Résultats FACTICES codés en dur (à remplacer plus tard par les
#     vrais résultats renvoyés par search_incidents()) ---
fake_search_results = [
    {
        "title": "Pod Kubernetes redémarre en boucle",
        "resolution": "Le readinessProbe était mal configuré, augmenter le délai initial l'a résolu.",
        "url": "https://github.com/example/repo/issues/101",
        "distance": 0.12,
    },
    {
        "title": "Container crash après déploiement",
        "resolution": "Le readinessProbe pointait vers le mauvais port.",
        "url": "https://github.com/example/repo/issues/205",
        "distance": 0.18,
    },
    {
        "title": "Pod OOMKilled en continu",
        "resolution": "Le problème venait des resources.limits trop bas, pas du readinessProbe.",
        "url": "https://github.com/example/repo/issues/312",
        "distance": 0.31,
    },
]


def build_diagnostic_prompt(user_question: str, similar_incidents: list) -> str:
    """
    Construit le texte du prompt à envoyer à une IA, à partir de la
    question de l'utilisateur et des incidents similaires trouvés.
    """
    incidents_text = ""
    for i, incident in enumerate(similar_incidents):
        incidents_text += (
            f"\nIncident {i + 1} :\n"
            f"- Titre : {incident['title']}\n"
            f"- Résolution : {incident['resolution']}\n"
            f"- Source : {incident['url']}\n"
        )

    prompt = f"""Tu es un assistant qui aide à diagnostiquer des bugs techniques.

Voici la question posée par l'utilisateur :
"{user_question}"

Voici {len(similar_incidents)} incidents similaires déjà résolus, trouvés dans l'historique :
{incidents_text}

Ta tâche :
1. Identifie la cause commune la plus probable entre ces incidents.
2. Indique un niveau de confiance selon le nombre de cas qui pointent vers la même cause.
3. Si un incident semble avoir une cause différente des autres, signale-le clairement.
4. Réponds dans ce format exact :

🔍 [nombre] incidents similaires trouvés
💡 Cause commune identifiée : [cause]
✅ Solution qui a fonctionné dans [X/Y] cas : [résumé + lien]
⚠️ Cas différent (si applicable) : [explication]
"""
    return prompt


if __name__ == "__main__":
    test_question = "Mon pod Kubernetes redémarre en boucle après un déploiement"

    prompt = build_diagnostic_prompt(test_question, fake_search_results)

    print("=" * 60)
    print("PROMPT GÉNÉRÉ (à envoyer à une IA) :")
    print("=" * 60)
    print(prompt)
