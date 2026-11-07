import os
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from routes.dass import dass_blueprint
from routes.personality import personality_blueprint
from routes.prediction import prediction_blueprint
from routes.research import research_blueprint


PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="/static")
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(dass_blueprint)
app.register_blueprint(personality_blueprint)
app.register_blueprint(prediction_blueprint)
app.register_blueprint(research_blueprint)


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/disclaimer")
def disclaimer():
    return send_from_directory(FRONTEND_DIR, "disclaimer.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "MATLAS API"})


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("MATLAS_DEBUG", "0") == "1",
        use_reloader=False,
    )
