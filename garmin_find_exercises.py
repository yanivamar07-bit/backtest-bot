#!/usr/bin/env python3
"""
Diagnostic: queries Garmin Connect exercise library to find valid category+exerciseName combos.
Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python3 garmin_find_exercises.py [keyword]
"""
import os, sys, json
try:
    from garminconnect import Garmin
except ImportError:
    sys.exit("pip3 install garminconnect")

EMAIL    = os.environ.get("GARMIN_EMAIL")
PASSWORD = os.environ.get("GARMIN_PASSWORD")
if not EMAIL or not PASSWORD:
    sys.exit("Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python3 garmin_find_exercises.py")

KEYWORDS = sys.argv[1:] or [
    "bench", "fly", "flye", "dip", "row", "pull", "shoulder", "lateral",
    "lat pulldown", "cable crossover", "pec deck", "reverse fly",
]

def main():
    TOKEN_FILE = os.path.expanduser("~/.garmin_tokens.json")
    print("Connexion...")
    client = Garmin(EMAIL, PASSWORD)
    client.login(tokenstore=TOKEN_FILE)
    print("Connecte.\n")

    found = {}

    for kw in KEYWORDS:
        print(f"Search: '{kw}'")
        try:
            # Garmin Connect exercise search endpoint
            result = client.connectapi(
                f"/workout-service/exercise/searchExercises",
                params={"q": kw, "locale": "fr-FR"}
            )
            exercises = result if isinstance(result, list) else result.get("exercises", result.get("results", []))
            for ex in exercises[:20]:
                cat  = ex.get("category", {})
                cat_key = cat.get("categoryKey") or cat.get("key") or str(cat)
                ex_key  = ex.get("exerciseKey") or ex.get("key") or ex.get("name") or str(ex)
                if cat_key not in found:
                    found[cat_key] = set()
                found[cat_key].add(ex_key)
                print(f"  category={cat_key!r:30s}  exercise={ex_key!r}")
        except Exception as ex:
            # Try alternative endpoint
            try:
                result = client.connectapi(
                    f"/workout-service/exercise/exercises",
                    params={"searchTerm": kw}
                )
                print(f"  Alt endpoint result type: {type(result)}")
                if isinstance(result, (list, dict)):
                    print(json.dumps(result, indent=2)[:500])
            except Exception as ex2:
                print(f"  Erreur: {ex}  |  Alt: {ex2}")
        print()

    print("\n=== RESUME ===")
    for cat, exs in sorted(found.items()):
        print(f"\ncategory: {cat!r}")
        for ex in sorted(exs):
            print(f"  exerciseName: {ex!r}")

if __name__ == "__main__":
    main()
