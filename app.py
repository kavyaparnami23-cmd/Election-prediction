"""
Author      : Kavya Parnami
Project     : ElectionPulse AI
Description : Flask Web Application — serves the ECI-style frontend
              and exposes a REST prediction API.

Run:
    python app.py
Then open http://localhost:5000
"""

import sys
import os

from flask import Flask, render_template, request, jsonify

# Make sure src/ is importable from project root
sys.path.insert(0, os.path.dirname(__file__))

from src.pipeline.prediction_pipeline import PredictionPipeline
from src.components.prediction import KNOWN_STATES

# ─────────────────────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────────────────────

app = Flask(__name__, template_folder="templates", static_folder="static")

# Lazy-load the pipeline once on first predict call
_pipeline: PredictionPipeline | None = None


def get_pipeline() -> PredictionPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = PredictionPipeline()
    return _pipeline


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main ECI-style page."""
    return render_template("index.html")


@app.route("/api/states", methods=["GET"])
def api_states():
    """Return the list of known states for the dropdown."""
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for s in KNOWN_STATES:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return jsonify({"states": sorted(unique)})


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    POST JSON body:
        {
            "year":     2019,
            "st_name":  "Maharashtra",
            "pc_no":    24,
            "pc_type":  "GEN",
            "cand_sex": "M",
            "electors": 150000
        }

    Returns:
        {
            "prediction":      1,
            "label":           "WINNER",
            "win_prob":        0.87,
            "predicted_votes": 120000   (optional)
        }
    """
    try:
        data = request.get_json(force=True)

        # Basic validation
        required = ["year", "st_name", "pc_no", "cand_sex", "electors"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        candidate = {
            "year":     int(data["year"]),
            "st_name":  str(data["st_name"]),
            "pc_no":    int(data["pc_no"]),
            "pc_type":  str(data.get("pc_type", "GEN")),
            "cand_sex": str(data["cand_sex"]).upper(),
            "electors": int(data["electors"]),
        }

        pipeline = get_pipeline()
        result = pipeline.predict_single(candidate)

        return jsonify(result)

    except FileNotFoundError as e:
        return jsonify({
            "error": "Model not found. Please train the model first.",
            "detail": str(e)
        }), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   ElectionPulse AI — Web Server")
    print("   Open http://localhost:5000 in your browser")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
