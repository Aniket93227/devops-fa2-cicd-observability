
from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "fa2_http_requests_total",
    "Total HTTP requests handled by the FA2 backend",
    ["method", "endpoint", "http_status"]
)


@app.after_request
def record_request(response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        http_status=str(response.status_code)
    ).inc()
    return response


@app.route("/")
def home():
    return jsonify({
        "application": "DevOps FA2",
        "message": "Backend is running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
