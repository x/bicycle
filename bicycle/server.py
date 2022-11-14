import json
import os
from random import sample
from time import sleep
from typing import Tuple

import openai
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, g, make_response, render_template, request
from flask.wrappers import Response

from .prompt import question_to_code

app = Flask(__name__)


def get_openai():
    if "openai" not in g:
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        g.openai = openai
    return g.openai


def get_test_data() -> Tuple[str, pd.DataFrame]:
    """Test data to be returned when the user enters the word 'test' in the prompt."""
    sleep(3)
    df = pd.DataFrame({k: sample(range(0, 100), 15) for k in ["Foo", "Bar", "Baz"]})
    code = "SELECT foo, bar, baz\nFROM test_table\nWHERE foo < 100"
    return code, df


@app.route("/")
def index():
    return render_template("index.html")


def format_response(code: str, df: pd.DataFrame) -> Response:
    """Format the response to be returned to the user."""
    html = df.to_html()
    html = html.replace('border="1"', "")  # Let pico.css do this
    resp = make_response(render_template("response.html", html=html, code=code))
    resp.headers["HX-Trigger-After-Swap"] = "afterResponse"
    return resp


@app.route("/query", methods=["POST"])
def query():
    question = request.form.get("query") or ""
    if len(question) < 10:
        return render_template("noquery.html")
    if question == "test":
        return format_response(*get_test_data())
    code = question_to_code(question)
    df = pd.DataFrame({k: sample(range(0, 100), 5) for k in ["Foo", "Bar", "Baz"]})
    return format_response(code, df)
