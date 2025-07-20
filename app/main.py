from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import uuid

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://admin:secret@localhost:27017/")
db = client["ilisten"]
collection = db["user_sentences"]

@app.teardown_appcontext
def close_mongo_client(exception):
    client.close()

@app.route("/store", methods=["POST"])
def store():
    try:
        payload = request.get_json(force=True)

        session_data = {
            "session_id": payload.get("session_id", str(uuid.uuid4())),
            "timestamp": payload.get("timestamp", datetime.utcnow().isoformat()),
            "sentence": payload["sentence"],
            "words": payload["words"]
        }

        user_id = payload["user_id"]

        collection.update_one(
            {"user_id": user_id},
            {"$push": {"sessions": session_data}},
            upsert=True
        )

        return jsonify({"status": "Saved", "data": session_data})

    except Exception as e:
        return jsonify({"error": f"Failed to store session: {str(e)}"}), 500

@app.route("/get/<user_id>", methods=["GET"])
def get_user_sessions(user_id):
    user_data = collection.find_one({"user_id": user_id}, {"_id": 0})
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": f"No data found for user_id: {user_id}"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
