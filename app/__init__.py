from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    @app.get("/")
    def index():
        return jsonify(service="meridian-pay", version="0.1.0"), 200

    @app.post("/api/echo")
    def echo():
        from flask import request

        payload = request.get_json(silent=True) or {}
        return jsonify(received=payload), 200

    return app
