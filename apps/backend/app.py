from flask import Flask
from flask_cors import CORS
from routes.api import api_blueprint
from routes.api_v2 import api_v2_blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for now
app.register_blueprint(api_blueprint)
app.register_blueprint(api_v2_blueprint)

if __name__ == "__main__":
    app.run(debug=True)