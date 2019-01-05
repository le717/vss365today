import os
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from dotenv import dotenv_values, find_dotenv


csrf = CSRFProtect()
db = SQLAlchemy()


def init_extensions(app):
    # Load the variables from the .env file into the app config
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        app.config[key] = (value if value != "" else None)

    # Determine the location for the database
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(
        os.path.join(base_dir, 'app.db')
    )

    # Load app exensions
    csrf.init_app(app)
    db.init_app(app)
