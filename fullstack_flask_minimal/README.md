# Minimal Flask App

This repository includes a minimal Python Flask app. Visit 'http://0.0.0.0:5000' in a browser. 

Using the following code in python to initialize the DB:
```python
from src.app import app, db
with app.app_context():
    db.create_all()
```

Start the flask app:
```shell
flask --app src.app run
```