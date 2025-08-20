from flask import Flask
from flask_cors import CORS
from routes.quote_routes import quote_bp
from routes.generate import generate_bp
from routes.manage import manage_bp 
from routes.video_routes import video_bp
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
CORS(app)

app.register_blueprint(quote_bp)
app.register_blueprint(generate_bp)
app.register_blueprint(video_bp)
app.register_blueprint(manage_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
