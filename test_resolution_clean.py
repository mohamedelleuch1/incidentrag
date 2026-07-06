import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}


def load_sample_from_local_file(filename="incidents_clean.json", n=5):
    with open(filename, "r", encoding="utf-8") as f:
        all_issues = json.load(f)
    return all_issues[:n]


def fetch_resolution_comment(issue):
    r = requests.get(issue["comments_url"], headers=HEADERS)

    if r.status_code != 200:
        print(f"⚠️ Impossible de récupérer les commentaires pour #{issue['id']}")
        return ""

    comments = r.json()

    if comments:
        for c in reversed(comments):
            if len(c["body"]) > 50:
                return c["body"]
        return comments[-1]["body"]

    return ""


if __name__ == "__main__":
    print("🔍 Chargement de 5 issues depuis incidents_clean.json...\n")
    sample = load_sample_from_local_file(n=5)

    for issue in sample:
        print("=" * 60)
        print(f"Issue #{issue['id']} : {issue['title']}")
        print(f"Lien : {issue['url']}")
        print(f"Nombre de commentaires : {issue['comments_count']}")

        my_resolution = fetch_resolution_comment(issue)
        already_stored = issue.get("resolution", "")

        preview = my_resolution[:150] + "..." if len(my_resolution) > 150 else my_resolution
        print(f"\n💡 Ma résolution trouvée :\n{preview}")

        match = "✅ Correspond" if my_resolution.strip() == already_stored.strip() else "⚠️ Différent de celui de Person A"
        print(f"\n{match}\n")