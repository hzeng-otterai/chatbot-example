import logging
import os

from flask import Flask

from .views import chat_bp
from .models import *


app = Flask(__name__)

if not os.getenv("RUNNING_IN_PRODUCTION"):
    app.logger.setLevel(logging.DEBUG)

app.register_blueprint(chat_bp)

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
print("DB path:", db_path)
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()