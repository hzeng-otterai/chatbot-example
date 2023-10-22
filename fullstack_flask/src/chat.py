import json
import os
import time
import datetime

import openai

from .search import search_news, search_text
from .models import db, ChatMessage


prompt_template = """You are a helpful assistant. Current time is {datetime}. I will give you a list of articles with title and text. Please answer questions.

Articles:
{context}

Answer:
"""

def call_chat_api(question):
    text_list = []

    #news_result_list = search_news(question)
    #time.sleep(1)
    web_result_list = search_text(question)
    time.sleep(1)

    for result in web_result_list:
        text = result["title"] + "\n" + result["body"]
        text_list.append(text)

    full_text = "\n\n".join(text_list)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        max_tokens=384,
        messages=[
            {"role": "system", "content": prompt_template.format(datetime=now, context=full_text)},
            {"role": "user", "content": question},
        ],
        stream=True,
    )

    answer_buffer = ""

    for event in response:
        token = event["choices"][0]["delta"].get("content")
        if token:
            answer_buffer += token
        yield event


    chat_message = ChatMessage(user_id=1, question=question, answer=answer_buffer)
    db.session.add(chat_message)
    db.session.commit()