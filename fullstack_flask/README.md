# Flask-based Chatbot

This repository includes a simple Python Flask app that streams responses from OpenAI
to an HTML/JS frontend using [NDJSON](http://ndjson.org/) over a [ReadableStream](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream).

The repository is designed for use with [Docker containers](https://www.docker.com/), both for local development and deployment. 🐳

## Start the app without docker
1. Using conda to create a new environment
    ```shell
    conda create -n myenv python=3.11
    ```

2. Install required packages
    ```shell
    pip install -r requirements-dev.txt
    ```

3. Start the flask app
    ```shell
    gunicorn app:app
    ```
    If you are starting it in a production environment, please use this:
    ```shell
    RUNNING_IN_PRODUCTION=1 gunicorn app:app
    ```
    Then use Ctrl-Z and the `bg && disown` to move it to background.

4. Click 'http://0.0.0.0:50505' in the terminal, which should open a new tab in the browser. You may need to navigate to 'http://localhost:50505' if that URL doesn't work.



## Start the app with docker

In addition to the `Dockerfile` that's used in production, this repo includes a `docker-compose.yaml` for
local development which creates a volume for the app code. That allows you to make changes to the code
and see them instantly.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/). If you opened this inside Github Codespaces or a Dev Container in VS Code, installation is not needed. ⚠️ If you're on an Apple M1/M2, you won't be able to run `docker` commands inside a Dev Container; either use Codespaces or do not open the Dev Container.

2. Make sure that the `.env` file exists and the correct OPENAI_API_KEY is set. 

3. Start the services with this command:

    ```shell
    docker compose up --build
    ```

4. Click 'http://0.0.0.0:50505' in the terminal, which should open a new tab in the browser. You may need to navigate to 'http://localhost:50505' if that URL doesn't work.


