from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"

# 🤖 LOAD AI MODEL (DECISION SUPPORT SYSTEM)
model = pickle.load(open("fire_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# 🧠 INIT DATABASE
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

init_db()

# 🔥 REPORT INCIDENT (SAVE TO DB)
@app.route('/report', methods=['POST'])
def report_incident():
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents (description, severity, latitude, longitude)
        VALUES (?, ?, ?, ?)
    """, (
        data['description'],
        data['severity'],
        data['lat'],
        data['lng']
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Incident saved to database!"})

# 📍 GET ALL INCIDENTS (GIS DATA)
@app.route('/incidents', methods=['GET'])
def get_incidents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
    rows = cursor.fetchall()

    conn.close()

    incidents = [
        {
            "id": r[0],
            "description": r[1],
            "severity": r[2],
            "lat": r[3],
            "lng": r[4],
            "timestamp": r[5]
        }
        for r in rows
    ]

    return jsonify(incidents)

# 🤖 AI DECISION SUPPORT SYSTEM (NEW FEATURE)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    description = data.get("description")

    # convert text → numeric features
    X = vectorizer.transform([description])

    # predict severity
    prediction = model.predict(X)[0]

    # 🧠 decision logic
    if prediction == "Low":
        recommendation = "Monitor situation. Low risk detected."
    elif prediction == "Medium":
        recommendation = "Prepare response unit. Possible escalation."
    else:
        recommendation = "ALERT! Immediate fire response required."

    return jsonify({
        "predicted_severity": prediction,
        "recommendation": recommendation
    })

# 🚀 RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)