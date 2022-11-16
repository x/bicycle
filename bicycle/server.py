import json
import logging
import os
import traceback as tb
from random import sample
from time import sleep
from typing import Tuple

import openai
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, g, make_response, render_template, request
from flask.wrappers import Response
from google.cloud import bigquery

from .prompt import question_to_code

app = Flask(__name__)


def get_openai():
    if "openai" not in g:
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]
        g.openai = openai
    return g.openai


def get_test_data() -> Tuple[str, str]:
    """Test data to be returned when the user enters the word 'test' in the prompt."""
    sleep(3)
    df = pd.DataFrame({k: sample(range(0, 100), 15) for k in ["Foo", "Bar", "Baz"]})
    code = "SELECT foo, bar, baz\nFROM test_table\nWHERE foo < 100"
    return code, df_to_table_html(df)


@app.route("/")
def index():
    return render_template("index.html")


def format_response(code: str, table_html: str) -> Response:
    """Format the response to be returned to the user."""
    resp = make_response(render_template("response.html", html=table_html, code=code))
    resp.headers["HX-Trigger-After-Swap"] = "afterResponse"
    return resp


def query_bq(code: str) -> pd.DataFrame:
    """Query BigQuery and return a dataframe."""
    client = bigquery.Client()
    query_job = client.query(code)
    df = query_job.to_dataframe()
    return df


def df_to_table_html(df: pd.DataFrame) -> str:
    """Convert a dataframe to HTML."""
    html = df.to_html()
    html = html.replace('border="1"', "")  # Let pico.css do this
    return html


@app.route("/query", methods=["POST"])
def query():
    question = request.form.get("query") or ""
    if question == "test":
        return format_response(*get_test_data())
    if len(question) < 10:
        return render_template("noquery.html")
    code = question_to_code(question)
    try:
        df = query_bq(code)
        table = df_to_table_html(df)
    except Exception as e:
        logging.exception(e)
        table = "<p>Sorry, I couldn't run that query.</p>"
        table += f"<pre><code>{tb.format_exc()}</code></pre>"
    return format_response(code, table)
