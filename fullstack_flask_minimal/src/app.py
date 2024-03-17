import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
print("DB path:", db_path)
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

from . import views
from . import models

if __name__ == "__main__":
    app.run(debug=True)
