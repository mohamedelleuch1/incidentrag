# ============================================================
# SCRIPT : extract_incidents.py
# BUT : Extraction complète de 150 issues diversifiées
#       (mix comments + updated) pour constituer le corpus
#       final du projet IncidentRAG
# ============================================================

import requests
import json
import time
from dotenv import load_dotenv
import os
from collections import Counter

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

REPO = "eclipse-mosquitto/mosquitto"


# ------------------------------------------------------------
# FONCTION 1 : Récupérer des issues selon un critère de tri donné
# ------------------------------------------------------------
def fetch_closed_issues(repo, max_issues=50, sort="comments"):
    """
    Récupère des issues fermées, triées selon le paramètre 'sort'.
    - sort="comments" -> les plus discutées en premier (bonnes résolutions)
    - sort="updated"  -> les plus récemment actives en premier (fraîcheur)
    """
    issues = []
    page = 1

    while len(issues) < max_issues:
        url = f"https://api.github.com/repos/{repo}/issues"
        params = {
            "state": "closed",
            "per_page": 30,
            "page": page,
            "sort": sort,
            "direction": "desc"
        }
        r = requests.get(url, headers=HEADERS, params=params)

        if r.status_code != 200:
            print(f"❌ Erreur API : {r.status_code} - {r.text}")
            break

        data = r.json()
        if not data:
            break

        for issue in data:
            if "pull_request" not in issue and issue["comments"] > 0:
                issues.append({
                    "id": issue["number"],
                    "title": issue["title"],
                    "body": issue["body"] or "",
                    "url": issue["html_url"],
                    "closed_at": issue["closed_at"],
                    "comments_count": issue["comments"],
                    "comments_url": issue["comments_url"],
                    "source_sort": sort
                })

        page += 1
        time.sleep(1)

        if page > 10:
            break

    return issues[:max_issues]


# ------------------------------------------------------------
# FONCTION 2 : Combiner plusieurs tris pour diversifier le corpus
# ------------------------------------------------------------
def fetch_diverse_issues(repo, total=150):
    all_issues = []
    seen_ids = set()

    print("📥 Lot 1/2 : issues les plus commentées...")
    lot1 = fetch_closed_issues(repo, max_issues=int(total * 0.6), sort="comments")
    for issue in lot1:
        if issue["id"] not in seen_ids:
            all_issues.append(issue)
            seen_ids.add(issue["id"])
    print(f"   → {len(lot1)} issues récupérées")

    print("📥 Lot 2/2 : issues les plus récemment mises à jour...")
    lot2 = fetch_closed_issues(repo, max_issues=int(total * 0.4), sort="updated")
    added = 0
    for issue in lot2:
        if issue["id"] not in seen_ids:
            all_issues.append(issue)
            seen_ids.add(issue["id"])
            added += 1
    print(f"   → {added} nouvelles issues ajoutées (doublons ignorés)")

    return all_issues


# ------------------------------------------------------------
# FONCTION 3 : Récupérer le commentaire de résolution d'une issue
# ------------------------------------------------------------
def fetch_resolution_comment(issue):
    r = requests.get(issue["comments_url"], headers=HEADERS)

    if r.status_code != 200:
        print(f"⚠️ Impossible de récupérer les commentaires pour l'issue #{issue['id']}")
        return ""

    comments = r.json()

    if comments:
        for c in reversed(comments):
            if len(c["body"]) > 50:
                return c["body"]
        return comments[-1]["body"]

    return ""


# ------------------------------------------------------------
# FONCTION 4 : Vérifier la diversité thématique du corpus final
# ------------------------------------------------------------
def check_diversity(issues):
    stopwords = {"the", "a", "an", "to", "in", "on", "of", "is", "for", "with",
                 "and", "not", "when", "after", "on", "at", "from", "does",
                 "why", "how", "can", "but", "are"}

    titles = [issue["title"].lower() for issue in issues]
    words = " ".join(titles).split()
    words = [w.strip(".,!?:;()[]'\"") for w in words if w not in stopwords and len(w) > 2]

    print("\n📊 Mots les plus fréquents dans les titres :")
    total = len(issues)
    for word, count in Counter(words).most_common(20):
        pct = (count / total) * 100
        print(f"   {word}: {count} ({pct:.1f}%)")


# ------------------------------------------------------------
# FONCTION PRINCIPALE
# ------------------------------------------------------------
def main():
    print(f"🔍 Extraction complète sur le repo : {REPO}")
    print("-" * 50)

    # Étape 1 : récupérer les issues diversifiées
    issues = fetch_diverse_issues(REPO, total=150)
    print(f"\n✅ Total : {len(issues)} issues uniques récupérées")

    if len(issues) == 0:
        print("❌ Aucune issue trouvée.")
        return

    # Étape 2 : vérifier la diversité thématique
    check_diversity(issues)

    # Étape 3 : récupérer la résolution de chaque issue
    print(f"\n📥 Récupération des résolutions ({len(issues)} appels, ~2 min)...")
    for i, issue in enumerate(issues):
        issue["resolution"] = fetch_resolution_comment(issue)
        time.sleep(0.5)
        if (i + 1) % 20 == 0:
            print(f"   ... {i + 1}/{len(issues)} traitées")

    # Étape 4 : sauvegarder le résultat final
    with open("incidents_clean.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print("\n" + "-" * 50)
    print(f"✅ Sauvegardé dans incidents_clean.json ({len(issues)} incidents)")
    print("👉 Fichier prêt à être partagé avec Personne B")


if __name__ == "__main__":
    main()