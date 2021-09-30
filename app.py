from flask import Flask, jsonify

app = Flask(__name__, static_folder='/', static_url_path="/")


@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


@app.route('/', defaults={'path': ''}, methods = ["POST", "GET"])
@app.route('/<path:path>', methods = ["POST"])
def catch_all(path):
    return app.send_static_file("index.html")
