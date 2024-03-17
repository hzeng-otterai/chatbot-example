# Flask-based Chatbot

This repository includes a simple Python Flask app that streams responses from OpenAI
to an HTML/JS frontend using [NDJSON](http://ndjson.org/) over a [ReadableStream](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream).

## Start the app
1. Using conda to create a new environment
    ```shell
    conda create -n myenv python=3.11
    ```

2. Install required packages
    ```shell
    pip install -r requirements-dev.txt
    ```
3. For the first time to start the app, you need to create the database
    Using the following code in python to initialize the DB:
    ```python
    from src.app import app, db
    with app.app_context():
        db.create_all()
    ```

4. Start the flask app
    ```shell
    gunicorn src.app:app
    ```

    If you want to start it in the background
    ```shell
    nohup gunicorn app:app &
    ```

5. Click 'http://0.0.0.0:50505' in the terminal, which should open a new tab in the browser. You may need to navigate to 'http://localhost:50505' if that URL doesn't work.

