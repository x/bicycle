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


def parse_sql_from_response_text(response: str) -> str:
    """Parse the SQL query from the response in a really bad way."""
    lines = response.splitlines()
    good_lines = []
    for line in lines:
        line = line.strip()
        # end case
        if "LIMIT" in line:
            good_lines.append(line)
            break
        # start case
        if (
            line.startswith("SELECT")
            or line.startswith("WITH")
            or line.startswith("VALUES")
        ):
            good_lines.append(line)
            continue
        # middle case
        if good_lines:
            good_lines.append(line)
    return "\n".join(lines)


ENGINE = "code-cushman-001"


def make_query_code(prompt: str) -> str:
    """Make a SQL query from the prompt text."""
    openai = get_openai()
    openai_prompt = f"""
-- BigQuery Table
-- State-level data for the number of cases and deaths from The New York Times. Sourced from https://github.com/nytimes/covid-19-data.
CREATE TABLE (
    fullname	mode	type	description
    date	NULLABLE	DATE	Date reported
    state_name	NULLABLE	STRING	State reported
    state_fips_code	NULLABLE	STRING	Standard geographic identifier for the state
    confirmed_cases	NULLABLE	INTEGER	The total number of confirmed cases of COVID-19
    deaths	NULLABLE	INTEGER	The total number of confirmed deaths of COVID-19
)
-- Query that answers: {prompt}
    """
    response = openai.Completion.create(
        engine=ENGINE,
        prompt=openai_prompt,
        max_tokens=1024,
    )
    response_text = response.choices[0].text  # type: ignore
    print("Response text was: " + response_text)
    code = parse_sql_from_response_text(response_text)
    print("Code was: " + code)
    return code


@app.route("/query", methods=["POST"])
def query():
    prompt = request.form.get("query") or ""
    if len(prompt) < 10:
        return render_template("noquery.html")
    if prompt == "test":
        return format_response(*get_test_data())
    code = make_query_code(prompt)
    df = pd.DataFrame({k: sample(range(0, 100), 5) for k in ["Foo", "Bar", "Baz"]})
    return format_response(code, df)


if __name__ == "__main__":
    get_openai()
    app.run(host="localhost")
