import json
import os

HIGHSCORE_FILE = "highscores.json"

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_highscores(scores):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def add_highscore(name, score):
    scores = load_highscores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # keep only top 10
    save_highscores(scores)
    return scores
