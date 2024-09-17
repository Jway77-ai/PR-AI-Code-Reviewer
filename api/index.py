import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Attempt to construct the PostgreSQL DATABASE_URL from environment variables
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("postgres_port", 5432)  # Default to 5432 if not specified
    db_name = os.getenv("POSTGRES_DATABASE")

    # Check if all PostgreSQL environment variables are available
    if db_user and db_password and db_host and db_name:
        database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        # Fallback to local SQLite database if PostgreSQL details are not available
        database_url = "sqlite:///test.db"
        print("PostgreSQL details not found. Falling back to local SQLite database.")

    # Configure SQLAlchemy with the constructed database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Apply ProxyFix for Vercel
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
