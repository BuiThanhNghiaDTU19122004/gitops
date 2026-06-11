import os
import random
import threading
import time

from flask import Flask, jsonify, render_template
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

VERSION = os.getenv("VERSION", "v1")
ERROR_RATE = float(os.getenv("ERROR_RATE", "0"))
LATENCY_SECONDS = float(os.getenv("LATENCY_SECONDS", "0"))
COUNTER_LOCK = threading.Lock()
CLICK_COUNT = 0

metrics = PrometheusMetrics(app)
metrics.info("api_build_info", "W9 API build information", version=VERSION)


def counter_payload():
    with COUNTER_LOCK:
        count = CLICK_COUNT

    return {
        "service": "api",
        "version": VERSION,
        "status": "ok",
        "count": count,
    }


@app.get("/")
def index():
    if LATENCY_SECONDS > 0:
        time.sleep(LATENCY_SECONDS)

    if random.random() < ERROR_RATE:
        return jsonify(service="api", version=VERSION, status="error"), 500

    return jsonify(service="api", version=VERSION, status="ok"), 200


@app.get("/app")
def frontend():
    return render_template("counter.html")


@app.get("/api/status")
def status():
    return jsonify(counter_payload()), 200


@app.get("/api/counter")
def get_counter():
    return jsonify(counter_payload()), 200


@app.post("/api/counter")
def increment_counter():
    global CLICK_COUNT

    with COUNTER_LOCK:
        CLICK_COUNT += 1

    return jsonify(counter_payload()), 200


@app.get("/healthz")
def healthz():
    return "ok", 200
