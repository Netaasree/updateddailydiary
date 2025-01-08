from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

# Basic configurations
app.config["MONGO_URI"] = "mongodb://localhost:27017/diary_db"

# CORS setup
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

mongo = PyMongo(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Save diary entry
@app.route('/diary', methods=['POST'])
def save_diary():
    diaries = mongo.db.diaries
    diaries.insert_one({
        'content': request.json['content']
    })
    return jsonify({'message': 'Diary saved successfully'})

# Get diary entries
@app.route('/diaries', methods=['GET'])
def get_diaries():
    diaries = mongo.db.diaries
    all_diaries = list(diaries.find())
    return jsonify([{'content': diary['content']} for diary in all_diaries])

if __name__ == '__main__':
    app.run(debug=True)
