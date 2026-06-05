#!/usr/bin/env python3
"""
Teste chaque categorie/exercice suspect avec un workout minimal 1x1.
Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python3 garmin_test_cats.py
"""
import os, sys, time
try:
    from garminconnect import Garmin
except ImportError:
    sys.exit("pip3 install garminconnect")

EMAIL    = os.environ.get("GARMIN_EMAIL")
PASSWORD = os.environ.get("GARMIN_PASSWORD")
if not EMAIL or not PASSWORD:
    sys.exit("Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python3 garmin_test_cats.py")

TOKEN_FILE = os.path.expanduser("~/.garmin_tokens.json")

S    = {"sportTypeId": 5, "sportTypeKey": "strength_training"}
WU   = {"unitId": 8, "unitKey": "kilogram", "factor": 1000.0}
NT   = {"workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target"}
SK   = {"strokeTypeId": 0, "strokeTypeKey": None, "displayOrder": 0}
EQ   = {"equipmentTypeId": 0, "equipmentTypeKey": None, "displayOrder": 0}
REPS = {"conditionTypeId": 10, "conditionTypeKey": "reps"}
LAP  = {"conditionTypeId": 1,  "conditionTypeKey": "lap.button"}
ITER = {"conditionTypeId": 7,  "conditionTypeKey": "iterations"}


def minimal_workout(cat, name):
    step = {
        "type": "ExecutableStepDTO", "stepOrder": 2,
        "stepType": {"stepTypeId": 3, "stepTypeKey": "interval"},
        "childStepId": 1, "description": None,
        "endCondition": REPS, "endConditionValue": 10.0,
        "targetType": NT, "targetValueOne": None, "targetValueTwo": 0.0,
        "targetValueUnit": None, "zoneNumber": None,
        "strokeType": SK, "equipmentType": EQ,
        "category": cat, "exerciseName": name,
        "weightValue": -1.0, "weightUnit": WU,
    }
    rest = {
        "type": "ExecutableStepDTO", "stepOrder": 3,
        "stepType": {"stepTypeId": 5, "stepTypeKey": "rest"},
        "childStepId": 1, "description": None,
        "endCondition": LAP, "endConditionValue": 0.0,
        "targetType": NT, "targetValueOne": None, "targetValueTwo": None,
        "targetValueUnit": None, "zoneNumber": None,
        "strokeType": SK, "equipmentType": EQ,
        "category": None, "exerciseName": None,
        "weightValue": -1.0, "weightUnit": WU,
    }
    group = {
        "type": "RepeatGroupDTO", "stepOrder": 1,
        "stepType": {"stepTypeId": 6, "stepTypeKey": "repeat"},
        "childStepId": 1, "numberOfIterations": 1,
        "workoutSteps": [step, rest],
        "endConditionValue": 1.0, "endCondition": ITER, "smartRepeat": False,
    }
    return {
        "workoutName": f"_TEST_{cat}_{name}",
        "description": "test", "sportType": S,
        "workoutSegments": [{"segmentOrder": 1, "sportType": S, "workoutSteps": [group]}],
    }


# Suspects — les 3 workouts qui echouent utilisent ces combos
TESTS = [
    # --- Lundi & Mercredi ---
    ("REAR_DELT",      "BENT_OVER_DUMBBELL_REAR_DELT_RAISE"),
    ("SHOULDER_PRESS", "SEATED_DUMBBELL_SHOULDER_PRESS"),
    ("SHOULDER_PRESS", "MACHINE_SHOULDER_PRESS"),
    ("DIP",            "WEIGHTED_DIP"),
    ("FLYE",           "PEC_DECK_FLYE"),
    ("FLYE",           "INCLINE_DUMBBELL_FLYE"),
    ("BENCH_PRESS",    "BARBELL_BENCH_PRESS"),
    # --- Mardi ---
    ("LAT_PULLDOWN",   "NEUTRAL_GRIP_LAT_PULLDOWN"),
    ("ROW",            "BARBELL_ROW"),
    ("CURL",           "PREACHER_CURL"),
    # --- Mercredi ---
    ("LATERAL_RAISE",  "CABLE_LATERAL_RAISE"),
]


def main():
    print("Connexion...")
    client = Garmin(EMAIL, PASSWORD)
    client.login(tokenstore=TOKEN_FILE)
    print("Connecte.\n")

    results = []
    created_ids = []

    for cat, name in TESTS:
        w = minimal_workout(cat, name)
        try:
            resp = client.upload_workout(w)
            wid = resp.get("workoutId") if isinstance(resp, dict) else None
            if wid:
                created_ids.append(wid)
            results.append((cat, name, True))
            print(f"  OK   {cat}/{name}")
        except Exception as ex:
            results.append((cat, name, False))
            print(f"  FAIL {cat}/{name}  →  {ex}")
        time.sleep(0.5)

    print(f"\nSuppression des {len(created_ids)} workouts de test...")
    for wid in created_ids:
        try:
            client.delete_workout(wid)
            time.sleep(0.3)
        except Exception:
            pass

    print("\n=== RÉSUMÉ ===")
    ok  = [(c, n) for c, n, ok in results if ok]
    bad = [(c, n) for c, n, ok in results if not ok]
    print(f"\nValides ({len(ok)}):")
    for c, n in ok:
        print(f"  ✓  {c}/{n}")
    print(f"\nInvalides ({len(bad)}):")
    for c, n in bad:
        print(f"  ✗  {c}/{n}")


if __name__ == "__main__":
    main()
