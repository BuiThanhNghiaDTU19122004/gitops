import os
import random
import time

from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

VERSION = os.getenv("VERSION", "v1")
ERROR_RATE = float(os.getenv("ERROR_RATE", "0"))
LATENCY_SECONDS = float(os.getenv("LATENCY_SECONDS", "0"))

metrics = PrometheusMetrics(app)
metrics.info("api_build_info", "W9 API build information", version=VERSION)


@app.get("/")
def index():
    if LATENCY_SECONDS > 0:
        time.sleep(LATENCY_SECONDS)

    if random.random() < ERROR_RATE:
        return jsonify(service="api", version=VERSION, status="error"), 500

    return jsonify(service="api", version=VERSION, status="ok"), 200


@app.get("/healthz")
def healthz():
    return "ok", 200

