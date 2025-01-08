from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

# Basic configurations
# Replace <username> and <password> with your actual MongoDB Atlas credentials
app.config["MONGO_URI"] = 'mongodb+srv://netaasree:Doreamon%40143@cluster1.gtow5.mongodb.net/DailyDiary?retryWrites=true&w=majority'

# CORS setup
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

# Initialize PyMongo
try:
    mongo = PyMongo(app)
    print("MongoDB connection initialized.")
except Exception as e:
    print("Failed to initialize MongoDB connection:", str(e))

@app.before_request
def initialize():
    if mongo.db is None:
        print("Failed to connect to MongoDB. Check your connection settings.")
    else:
        print("Successfully connected to MongoDB.")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Save diary entry
@app.route('/diary', methods=['POST'])
def save_diary():
    try:
        diaries = mongo.db.diaries  # This will create the 'diaries' collection automatically when inserting data
        print("MongoDB Diaries Collection:", diaries)  # Debugging statement
        
        # Check if the content is provided
        content = request.json.get('content')
        print("Content from Request:", content)  # Debugging statement
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Insert the diary entry, if the 'diaries' collection doesn't exist, it will be created automatically
        diaries.insert_one({'content': content})
        return jsonify({'message': 'Diary saved successfully'})
    except Exception as e:
        print("Exception Occurred:", str(e))  # Debugging statement
        return jsonify({'error': str(e)}), 500

# Get diary entries
@app.route('/diaries', methods=['GET'])
def get_diaries():
    try:
        diaries = mongo.db.diaries  # Reference to 'diaries' collection
        print("MongoDB Diaries Collection:", diaries)  # Debugging statement
        
        # Check if there are any diary entries in the collection
        if diaries.count_documents({}) == 0:
            return jsonify({'message': 'No diaries found.'})

        all_diaries = list(diaries.find())
        return jsonify([{'content': diary['content']} for diary in all_diaries])
    except Exception as e:
        print("Exception Occurred:", str(e))  # Debugging statement
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
