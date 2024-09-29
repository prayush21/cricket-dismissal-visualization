from flask import Flask
from flask_cors import CORS

from routes.api import api_blueprint

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
