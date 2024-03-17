import json
from flask import Blueprint, Response, jsonify, render_template, request, stream_with_context

from .models import User
#from .chat_api import call_chat
from .chat_langchain import call_chat


chat_bp = Blueprint("chat", __name__, template_folder="templates", static_folder="static")

@chat_bp.get("/")
def index():
    return render_template("index.html")

@chat_bp.post("/chat")
def chat_handler():
    request_message = request.json["message"]

    @stream_with_context
    def response_stream():
        for chunk in call_chat(request_message):
            # returning a json format for easier encoding
            yield json.dumps(chunk, ensure_ascii=False) + "\n"

    return Response(response_stream())

@chat_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    # Retrieve user data from the database and return a JSON response
    return {"name": "Example Name"}

