import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load("models/rf_model.joblib")
with open("models/progress_curve.json") as f:
    progress_curve = {int(k): v for k, v in json.load(f).items()}

GOAL = 10000
CHECKPOINTS = sorted(progress_curve)

@app.route("/")
def index():
    return send_from_directory(app.root_path, "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    try:
        minute_of_day = int(data["minute_of_day"])
        steps_so_far = int(data["steps_so_far"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="minute_of_day and steps_so_far must be whole numbers"), 400
    if not (0 <= minute_of_day < 1440) or not (0 <= steps_so_far <= 100000):
        return jsonify(error="values out of range"), 400

    X = pd.DataFrame([[minute_of_day, steps_so_far]],
                     columns=["MinuteOfDay", "StepsSoFar"])
    prob = float(model.predict_proba(X)[0, 1])

    return jsonify(
        probability=round(prob, 3),
        will_reach=prob >= 0.5,
        steps_remaining=max(GOAL - steps_so_far, 0),
        in_trained_range=480 <= minute_of_day <= 1290,
    )


@app.route("/curve")
def curve():
    return jsonify(
        goal=GOAL,
        minutes=CHECKPOINTS,
        progress=[progress_curve[c] for c in CHECKPOINTS],
    )


if __name__ == "__main__":
    app.run(port=5000)