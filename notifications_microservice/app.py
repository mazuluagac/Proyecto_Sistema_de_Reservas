from flask import Flask, jsonify, request
from pymongo import MongoClient

# Initialize the Flask application
app = Flask(__name__)

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["notifications_db"]
notifications_collection = db["notifications"]

@app.route('/')
def home():
    return jsonify({"message": "Microservicio de Notificaciones en Flask funcionando 🚀"})




if __name__ == '__main__':
    app.run(debug=True)  