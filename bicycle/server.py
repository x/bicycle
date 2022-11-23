import logging
import math
import os
import sqlite3
import traceback as tb
from pathlib import Path
from random import sample
from string import Template
from typing import Tuple

import openai
import pandas as pd
import sqlparse
from dotenv import load_dotenv
from flask import Flask, make_response, render_template, request
from flask.wrappers import Response

SQLLITE_DB_PATH = "data/citibike.db"
"""The path to the SQLite DB."""

ENGINE = "code-davinci-002"
"""The OpenAI engine we're using."""

BOT_NAME = "BOB"
"""The name of the bot."""


# Setup
app = Flask(
    __name__,
    static_url_path="",
    static_folder="static",
    template_folder="templates",
)
load_dotenv()
logging.getLogger("bicycle").setLevel(logging.INFO)


def get_test_data() -> Tuple[str, str, str]:
    """Test data to be returned when the user enters the word 'test' in the prompt."""
    df = pd.DataFrame({k: sample(range(0, 100), 5) for k in ["Foo", "Bar", "Baz"]})
    code = "SELECT foo, bar, baz\nFROM test_table\nWHERE foo < 100"
    return "Is this a test?", code, df_to_table_html(df)


def clean_code(code: str) -> str:
    """Clean up the SQL to look nice."""
    code = code.replace(f"{BOT_NAME}:", "").replace("User:", "")
    code = sqlparse.format(
        code,
        reindent=True,
        keyword_case="upper",
        strip_comments=True,
    )
    code = code.replace(
        "bigquery-PUBLIC-data", "bigquery-public-data"
    )  # bad sqlparse.format
    return code


def question_to_code(question: str) -> str:
    prompt_str = (
        Path("./bicycle/prompts/preamble01.txt.tpl").read_text()
        + Path("./bicycle/prompts/citibike.txt.tpl").read_text()
    )
    prompt = Template(prompt_str).substitute(bot_name=BOT_NAME, question=question)
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Completion.create(
        engine=ENGINE,
        prompt=prompt,
        max_tokens=512,
        stop="________",
        n=1,
        temperature=0.,
        best_of=4,
    )
    return response.choices[0].text  # type: ignore


def setup_math_functions(conn) -> None:
    """Setup the math functions for SQLite.

    It's not clear to me why this extention isn't there by default....

    See:
        https://www.sqlite.org/lang_mathfunc.html

    Interestingly, this could be a cool way for us to extend the SQL.
    """
    conn.create_function("log", 2, math.log)
    conn.create_function("sqrt", 1, math.sqrt)
    conn.create_function("pow", 2, math.pow)
    conn.create_function("exp", 1, math.exp)
    conn.create_function("pi", 0, math.pi)
    conn.create_function("acos", 1, math.acos)
    conn.create_function("cos", 1, math.cos)
    conn.create_function("asin", 1, math.asin)
    conn.create_function("sin", 1, math.sin)
    conn.create_function("radians", 1, lambda d: d * math.pi / 180)


def query_sqlite(code: str) -> pd.DataFrame:
    """Query SQLite and return a dataframe."""
    conn = sqlite3.connect(SQLLITE_DB_PATH)
    setup_math_functions(conn)
    res = conn.execute(code)
    df = pd.DataFrame(res.fetchall(), columns=[x[0] for x in res.description])
    return df


def df_to_table_html(df: pd.DataFrame) -> str:
    """Convert a dataframe to HTML."""
    html = df.to_html()
    html = html.replace('border="1"', "")  # Let pico.css do this
    return html


def format_response(question: str, code: str, table_html: str) -> Response:
    """Format the response to be returned to the user."""
    code = clean_code(code)
    resp = make_response(
        render_template("response.html", html=table_html, code=code, question=question)
    )
    resp.headers["HX-Trigger-After-Swap"] = "afterResponse"
    return resp


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    question = request.form.get("query") or ""
    if question == "test":
        return format_response(*get_test_data())
    if len(question) < 10:
        return render_template("noquery.html")
    code = question_to_code(question).replace("```", "")
    print(f"{question=} {code=}")
    try:
        df = query_sqlite(code)
        table = df_to_table_html(df)
    except Exception as e:
        logging.exception(e)
        table = "<p>Sorry, I couldn't run that query.</p>"
        table += f"<pre><code>{tb.format_exc()}</code></pre>"
    return format_response(question, code, table)
