#!/usr/bin/env python3
"""
Gorilla Hypertrophy — Garmin Connect workout creator
Format correct : RepeatGroupDTO avec vrais noms d'exercices.
Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python3 garmin_workouts.py
"""
import os, sys, time
try:
    from garminconnect import Garmin
except ImportError:
    sys.exit("pip3 install garminconnect")

EMAIL    = os.environ.get("GARMIN_EMAIL")
PASSWORD = os.environ.get("GARMIN_PASSWORD")
if not EMAIL or not PASSWORD:
    sys.exit("Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python3 garmin_workouts.py")

S    = {"sportTypeId": 5, "sportTypeKey": "strength_training"}
WU   = {"unitId": 8, "unitKey": "kilogram", "factor": 1000.0}
NT   = {"workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target"}
SK   = {"strokeTypeId": 0, "strokeTypeKey": None, "displayOrder": 0}
EQ   = {"equipmentTypeId": 0, "equipmentTypeKey": None, "displayOrder": 0}
REPS = {"conditionTypeId": 10, "conditionTypeKey": "reps"}
TIME = {"conditionTypeId": 2,  "conditionTypeKey": "time"}
LAP  = {"conditionTypeId": 1,  "conditionTypeKey": "lap.button"}
ITER = {"conditionTypeId": 7,  "conditionTypeKey": "iterations"}


class WB:
    """Workout Builder — construit des workouts au format RepeatGroupDTO."""
    def __init__(self): self.o = 0; self.c = 0; self.g = []
    def _o(self): self.o += 1; return self.o
    def _c(self): self.c += 1; return self.c

    def add(self, iters, exs):
        go = self._o(); cid = self._c(); inner = []
        for cat, name, val, w, timed in exs:
            inner.append({
                "type": "ExecutableStepDTO",
                "stepOrder": self._o(),
                "stepType": {"stepTypeId": 3, "stepTypeKey": "interval"},
                "childStepId": cid,
                "description": None,
                "endCondition": TIME if timed else REPS,
                "endConditionValue": float(val),
                "targetType": NT,
                "targetValueOne": None, "targetValueTwo": 0.0, "targetValueUnit": None,
                "zoneNumber": None, "strokeType": SK, "equipmentType": EQ,
                "category": cat, "exerciseName": name,
                "weightValue": float(w), "weightUnit": WU,
            })
        inner.append({
            "type": "ExecutableStepDTO",
            "stepOrder": self._o(),
            "stepType": {"stepTypeId": 5, "stepTypeKey": "rest"},
            "childStepId": cid,
            "description": None,
            "endCondition": LAP, "endConditionValue": 0.0,
            "targetType": NT,
            "targetValueOne": None, "targetValueTwo": None, "targetValueUnit": None,
            "zoneNumber": None, "strokeType": SK, "equipmentType": EQ,
            "category": None, "exerciseName": None,
            "weightValue": -1.0, "weightUnit": WU,
        })
        self.g.append({
            "type": "RepeatGroupDTO",
            "stepOrder": go,
            "stepType": {"stepTypeId": 6, "stepTypeKey": "repeat"},
            "childStepId": cid,
            "numberOfIterations": iters,
            "workoutSteps": inner,
            "endConditionValue": float(iters),
            "endCondition": ITER,
            "smartRepeat": False,
        })

    def build(self, name, desc):
        return {
            "workoutName": name, "description": desc, "sportType": S,
            "workoutSegments": [{"segmentOrder": 1, "sportType": S, "workoutSteps": self.g}],
        }


def e(cat, name, val, w=-1, timed=False):
    return (cat, name, val, w, timed)


def build_lundi():
    b = WB()
    b.add(5, [e("BENCH_PRESS", "BARBELL_BENCH_PRESS",          6, 77.5)])
    b.add(4, [e("BENCH_PRESS", "INCLINE_DUMBBELL_BENCH_PRESS", 9, 29)])
    b.add(4, [e(None, None,                                   10, 15)])
    b.add(4, [
        e("FLYE", "PEC_DECK_FLYE",        15),
        e("FLYE", "INCLINE_DUMBBELL_FLYE", 12, 13),
    ])
    b.add(4, [
        e("SHOULDER_PRESS", "SEATED_DUMBBELL_SHOULDER_PRESS",    10, 20),
        e("LATERAL_RAISE",  "DUMBBELL_LATERAL_RAISE",            17,  8),
        e("FLYE",           "BENT_OVER_DUMBBELL_REAR_DELT_RAISE", 15,  6),
    ])
    b.add(3, [
        e("TRICEPS_EXTENSION", "EZ_BAR_SKULL_CRUSHER", 10, 30),
        e("TRICEPS_EXTENSION", "ROPE_PUSHDOWN",         15),
    ])
    return b.build(
        "Push Silverback — Pecs · Epaules · Triceps",
        "Dev couche 5x6@77.5 | Dev incline 4x9@29 | Dips lestes 4x10@+15 | "
        "Biset Pec Deck+Ecartes x4 | Cannonball triset x4 | Biset Triceps x3 | Marche inclinee 20min",
    )


def build_mardi():
    b = WB()
    b.add(5, [e("PULL_UP", "PULL_UP",    8)])
    b.add(5, [e("ROW",     "BARBELL_ROW", 8, 75)])
    b.add(4, [
        e(None,  None,               11),
        e("ROW", "SEATED_CABLE_ROW", 11),
    ])
    b.add(4, [
        e("CURL", "EZ_BAR_CURL",           10, 32.5),
        e("CURL", "INCLINE_DUMBBELL_CURL", 12, 12),
    ])
    b.add(3, [
        e("CURL", "HAMMER_CURL",   12, 16),
        e("CURL", "PREACHER_CURL", 12),
    ])
    b.add(1, [e("CURL", "CABLE_BICEPS_CURL", 50)])
    return b.build(
        "Pull Gorilla — Dos · Biceps",
        "Tractions 5x8 | Rowing barre 5x8@75 | Biset tirage x4 | "
        "Biset curl EZ+incline x4 | Biset marteau+pupitre x3 | Finisher curl 50 | Velo 20min",
    )


def build_mercredi():
    b = WB()
    b.add(5, [e("SHOULDER_PRESS", "MACHINE_SHOULDER_PRESS", 9)])
    b.add(5, [
        e("LATERAL_RAISE", "DUMBBELL_LATERAL_RAISE", 15, 8),
        e("FLYE",          "REAR_DELT_FLY",          15),
        e("LATERAL_RAISE", "CABLE_LATERAL_RAISE",    15),
    ])
    b.add(4, [
        e("CURL",              "EZ_BAR_CURL",          10),
        e("TRICEPS_EXTENSION", "EZ_BAR_SKULL_CRUSHER", 10),
    ])
    b.add(4, [
        e("CURL",              "PREACHER_CURL", 12),
        e("TRICEPS_EXTENSION", "ROPE_PUSHDOWN", 15),
    ])
    b.add(3, [
        e("CURL",              "INCLINE_DUMBBELL_CURL",      12, 12),
        e("TRICEPS_EXTENSION", "OVERHEAD_TRICEPS_EXTENSION", 15),
    ])
    b.add(4, [
        e("CRUNCH",    "CABLE_CRUNCH",      15),
        e("LEG_RAISE", "HANGING_LEG_RAISE", 15),
    ])
    return b.build(
        "Shoulders & Arms Titan — Epaules · Bras · Abdos",
        "Shoulder press machine 5x9 | Giant set epaules x5 | Biset curl+front x4 | "
        "Biset pupitre+pushdown x4 | Biset incline+overhead x3 | Abdos x4 | Rameur 15min",
    )


def build_vendredi():
    b = WB()
    b.add(5, [e("BENCH_PRESS", "INCLINE_DUMBBELL_BENCH_PRESS", 8, 30)])
    b.add(5, [e("PULL_UP",     "WEIGHTED_PULL_UP",              7, 15)])
    b.add(4, [
        e("BENCH_PRESS", "MACHINE_CHEST_PRESS",    12),
        e("ROW",         "INCLINE_DUMBBELL_ROW",   12),
    ])
    b.add(4, [
        e("FLYE", "CABLE_CROSSOVER",  15),
        e("ROW",  "SEATED_CABLE_ROW", 12),
    ])
    b.add(4, [
        e("LATERAL_RAISE", "DUMBBELL_LATERAL_RAISE", 15,  8),
        e("CURL",          "HAMMER_CURL",             12, 16),
    ])
    b.add(1, [
        e("PUSH_UP", "PUSH_UP",  50),
        e("PULL_UP", "PULL_UP",  25),
    ])
    return b.build(
        "Upper Mass Monster — Pecs · Dos · Bras",
        "Dev incline 5x8@30 | Tractions lestees 5x7@+15 | Bisets pecs/dos x4 | "
        "Ecartes+tirage x4 | Elev lat+curl x4 | Finisher 50 pompes+25 tractions | Marche 20min",
    )


def build_dimanche():
    b = WB()
    b.add(4, [
        e("CURL",              "EZ_BAR_CURL",          9, 35),
        e("TRICEPS_EXTENSION", "EZ_BAR_SKULL_CRUSHER", 9, 30),
    ])
    b.add(4, [
        e("CURL",              "INCLINE_DUMBBELL_CURL", 12, 12),
        e("TRICEPS_EXTENSION", "ROPE_PUSHDOWN",         15),
    ])
    b.add(4, [
        e("CURL",              "HAMMER_CURL",                12, 16),
        e("TRICEPS_EXTENSION", "OVERHEAD_TRICEPS_EXTENSION", 15),
    ])
    b.add(1, [
        e("CURL",              "CABLE_BICEPS_CURL", 50),
        e("TRICEPS_EXTENSION", "ROPE_PUSHDOWN",     50),
    ])
    b.add(4, [
        e("CRUNCH",    "CABLE_CRUNCH",      15),
        e("LEG_RAISE", "HANGING_LEG_RAISE", 15),
    ])
    b.add(3, [e("PLANK", "PLANK", 60, timed=True)])
    return b.build(
        "Arms & Abs Annihilation — Bras · Abdos",
        "Biset curl EZ lourd+front x4 | Biset incline+pushdown x4 | "
        "Biset marteau+overhead x4 | Finisher 50+50 | Abdos x4 | Gainage 3x1min | Velo 20min",
    )


OLD = [
    "Pecs · Epaules · Triceps", "Dos · Biceps",
    "Epaules · Bras · Abdos",   "Pecs · Dos · Bras", "Bras · Abdos",
    "Push Silverback — Pecs · Epaules · Triceps",
    "Pull Gorilla — Dos · Biceps",
    "Shoulders & Arms Titan — Epaules · Bras · Abdos",
    "Upper Mass Monster — Pecs · Dos · Bras",
    "Arms & Abs Annihilation — Bras · Abdos",
]

WORKOUTS = [
    build_lundi(), build_mardi(), build_mercredi(),
    build_vendredi(), build_dimanche(),
]


TOKEN_FILE = os.path.expanduser("~/.garmin_tokens.json")


def main():
    print("Connexion...")
    client = Garmin(EMAIL, PASSWORD)
    client.login(tokenstore=TOKEN_FILE)
    print(f"Connecte. (tokens sauvegardes dans {TOKEN_FILE})\n")

    print("Suppression anciens workouts...")
    try:
        for w in client.get_workouts(0, 100):
            if w.get("workoutName") in OLD:
                client.delete_workout(w["workoutId"])
                print(f"  Supprime : {w['workoutName']}")
                time.sleep(0.5)
    except Exception as ex:
        print(f"  Erreur suppression : {ex}")

    print("\nCreation workouts...")
    for w in WORKOUTS:
        print(f"  {w['workoutName']}")
        try:
            client.upload_workout(w)
            print("    OK")
        except Exception as ex:
            print(f"    Erreur : {ex}")
        time.sleep(1)

    print("\nTermine ! Garmin Connect > Entrainement > Workouts, puis sync Bluetooth.")


if __name__ == "__main__":
    main()
