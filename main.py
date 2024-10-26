from flask import Flask, request, jsonify

app = Flask(__name__)

# Ustawienia tokenu
SECRET_TOKEN = "supersecrettoken123"

# Endpoint zabezpieczony tokenem
@app.route("/secure-data", methods=["GET"])
def secure_data():
    token = request.headers.get("Authorization")
    if token == f"Bearer {SECRET_TOKEN}":
        return jsonify({"message": "sukces"})
    else:
        return jsonify({"detail": "Niepoprawny token"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
