#!/usr/bin/env python3
"""
Gorilla Hypertrophy — création des séances dans Garmin Connect.

Prérequis :
    pip install garminconnect

Usage :
    GARMIN_EMAIL=ton@email.com GARMIN_PASSWORD=motdepasse python garmin_workouts.py
"""

import os
import sys
import time

try:
    from garminconnect import Garmin
except ImportError:
    sys.exit("pip install garminconnect")

EMAIL    = os.environ.get("GARMIN_EMAIL")
PASSWORD = os.environ.get("GARMIN_PASSWORD")

if not EMAIL or not PASSWORD:
    sys.exit("Usage: GARMIN_EMAIL=xxx GARMIN_PASSWORD=yyy python garmin_workouts.py")

STRENGTH = {"sportTypeId": 4, "sportTypeKey": "strength_training"}


def step(order: int, note: str, reps: int = 0, rest_sec: int = 0):
    if rest_sec:
        return {
            "stepOrder": order,
            "stepType": {"stepTypeId": 4, "stepTypeKey": "rest"},
            "durationValue": rest_sec,
            "durationValueType": {"durationTypeId": 2, "durationTypeKey": "time"},
            "description": f"Repos {rest_sec}s",
        }
    return {
        "stepOrder": order,
        "stepType": {"stepTypeId": 3, "stepTypeKey": "interval"},
        "description": note,
        "repetitionValue": reps if reps else 1,
        "repetitionValueType": {"repetitionTypeId": 3, "repetitionTypeKey": "repetitions"},
    }


def workout(name: str, description: str, steps: list) -> dict:
    return {
        "workoutName": name,
        "description": description,
        "sportType": STRENGTH,
        "workoutSegments": [{
            "segmentOrder": 1,
            "sportType": STRENGTH,
            "workoutSteps": steps,
        }],
    }


WORKOUTS = [
    workout(
        "LUNDI — Push Silverback (Pecs)",
        "Pecs priorité | Épaules | Triceps | Cardio 20 min marche inclinée",
        [
            step(1,  "Développé couché barre — échauff progressif", 10),
            step(2,  "Développé couché barre 6×6 lourd", 6),
            step(3,  "", rest_sec=120),
            step(4,  "Développé incliné haltères 5×8-10", 9),
            step(5,  "", rest_sec=90),
            step(6,  "Dips lestés 5×8-12", 10),
            step(7,  "", rest_sec=90),
            step(8,  "Pec Deck 4×15-20 + dernière série dropset", 17),
            step(9,  "CANNONBALL ×4 — Dév militaire 20kg ×10 | Élév lat 8kg ×20 | Oiseau 6kg ×15", 1),
            step(10, "", rest_sec=60),
            step(11, "TRICEPS ×4 — Barre front ×10 | Pushdown corde ×15 | Dips banc max", 1),
            step(12, "", rest_sec=45),
            step(13, "Cardio : marche inclinée 20 min — 12% / 5,5 km/h", 1),
        ],
    ),
    workout(
        "MARDI — Pull Gorilla (Dos + Bras)",
        "Dos lourd | Biceps | Finisher preacher curl dropset | Vélo 20 min",
        [
            step(1,  "Tractions pronation 5×6-10", 8),
            step(2,  "Rowing barre 5×8 lourd", 8),
            step(3,  "", rest_sec=120),
            step(4,  "Tirage vertical prise neutre 4×10-12", 11),
            step(5,  "Rowing machine convergente 4×10-12", 11),
            step(6,  "BICEPS ×4 — Curl EZ 30-35kg ×10 | Curl incliné 12-14kg ×12 | Curl marteau 16kg ×12", 1),
            step(7,  "", rest_sec=60),
            step(8,  "Finisher : Preacher curl machine 12 reps → -20% → max → -20% → max", 1),
            step(9,  "Cardio : vélo 20 min", 1),
        ],
    ),
    workout(
        "MERCREDI — Shoulders & Arms Titan",
        "Épaules | Bras en bisets | Finisher 100 élév lat + 50 curls | Rameur 15 min",
        [
            step(1,  "Shoulder Press Machine 5×8-10", 9),
            step(2,  "Élévations latérales poulie 5×15", 15),
            step(3,  "Reverse Pec Deck 4×15", 15),
            step(4,  "Biset ×4 — Curl EZ + Barre front", 1),
            step(5,  "", rest_sec=60),
            step(6,  "Biset ×4 — Preacher curl + Pushdown corde", 1),
            step(7,  "", rest_sec=60),
            step(8,  "Biset ×3 — Curl incliné + Extension au-dessus de la tête", 1),
            step(9,  "Finisher : 100 élévations latérales", 100),
            step(10, "Finisher : 50 curls marteau", 50),
            step(11, "Cardio : rameur 15 min", 1),
        ],
    ),
    workout(
        "VENDREDI — Upper Mass Monster",
        "Pecs + Dos | Bras | Cardio 15 min",
        [
            step(1,  "Développé incliné haltères 5×8", 8),
            step(2,  "Tractions lestées 5×6-8", 7),
            step(3,  "", rest_sec=120),
            step(4,  "Développé convergent machine 4×12", 12),
            step(5,  "Rowing poitrine appuyée 4×12", 12),
            step(6,  "Écartés poulie 4×15", 15),
            step(7,  "Tirage horizontal poulie 4×12", 12),
            step(8,  "Biset bras ×4 — Curl marteau + Extension corde", 1),
            step(9,  "Cardio 15 min (vélo ou rameur)", 1),
        ],
    ),
    workout(
        "DIMANCHE — Legs & Core (OBLIGATOIRE)",
        "Jambes | Abdos | Vélo 20 min",
        [
            step(1,  "Squat 5×5", 5),
            step(2,  "", rest_sec=180),
            step(3,  "Presse 4×15", 15),
            step(4,  "Soulevé de terre roumain 4×10", 10),
            step(5,  "Leg curl 4×15", 15),
            step(6,  "Mollets 5×20", 20),
            step(7,  "Abdos — Crunch câble 4×15 | Relevés de jambes 4×15 | Gainage 3×1 min", 1),
            step(8,  "Cardio : vélo 20 min", 1),
        ],
    ),
]


def main():
    print("Connexion à Garmin Connect...")
    client = Garmin(EMAIL, PASSWORD)
    client.login()
    print("Connecté.\n")

    for w in WORKOUTS:
        print(f"  Création : {w['workoutName']}")
        try:
            client.add_workout(w)
            print("    ✓ OK")
        except Exception as e:
            print(f"    ✗ Erreur : {e}")
        time.sleep(1)

    print("\nTerminé — ouvre Garmin Connect → Entraînement → Workouts pour les voir.")
    print("Synchronise ta montre via Bluetooth pour les avoir directement dessus.")


if __name__ == "__main__":
    main()
