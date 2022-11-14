import json
import os

import openai

from .tables import (
    CITIBIKE_STATIONS_FIELDS,
    CITIBIKE_STATIONS_NAME,
    CITIBIKE_TRIPS_FIELDS,
    CITIBIKE_TRIPS_NAME,
)

GOPHER_PROMPT_PREAMBLE = """User: What can you tell me about cell biology?
Gopher: Sure, I can tell you some basic facts. The nucleus is the central part of the cell, and
it contains the DNA. Each chromosome contains many genes. Cells divide when they
reproduce, and the DNA is duplicated before this happens. A group of similar cells is
called a tissue.
User: What is the technical name for single-cell organisms?
Gopher: They're known as prokaryotes.
User: Are humans prokaryotes?
Gopher: No, they're eukaryotes.
User: What's an example of a prokaryote?
Gopher: Well, bacteria and archaea are prokaryotes.
User: What's a common species of bacteria that lives in the gut?
Gopher: Well, I believe it's Escherichia coli.
User: Is E. Coli always dangerous?
Gopher: Not always - but in some cases, it can be pathogenic. That means it can cause harm to
the body.
User: Which strains are dangerous?
Gopher: The most dangerous ones are serotype O157:H7 and serotype O111:H.
User: Can you give me a link where I can learn more?
Gopher: Yes, here you go:
https://en.wikipedia.org/wiki/Escherichia_coli_O157:H7
User: Can you confidently tell me who won the Women’s US Open in 2021?
Gopher: Sure! It was Naomi Osaka.
User: Are there any French-speaking countries in South America?
Gopher: No.
User: Do you know the result of e**(i*pi)+1?
Gopher: Yes it's 2.
User: Do you have any uncertainty about your answers so far?
Gopher: No."""
"""See: https://arxiv.org/pdf/2112.11446.pdf"""

SQL_PREAMBLE = """User: Given the BigQuery table 'users' with fields '[{"name": "fullname", "mode": "NULLABLE", "type": "STRING", "description": "Full name of the person", "fields": []}, {"name": "age", "mode": "NULLABLE", "type": "INTEGER", "description": "Age of the person", "fields": []}]' what's a BigQuery query that answers the question 'What is the average age of people named John?'
Gopher: SELECT AVG(age) FROM `users` WHERE name = 'John'
User: Given the BigQuery table 'boats' with fields '[{"name": "id", "mode": "REQUIRED", "type": "INTEGER", "description": "Unique identifier of the boat", "fields": []}, {"name": "name", "mode": "NULLABLE", "type": "STRING", "description": "The name of the boat", "fields": []}]' and the table 'sailors' with fields '[{"name": "name", "mode": "NULLABLE", "type": "STRING", "description": "The name of the sailor.", "fields": []}, {"name": "boat_id", "mode": "REQUIRED", "type": "INTEGER", "description": "The boat that the sailor crews on.", "fields": []}, {"name": "age", "mode": "NULLABLE", "type": "INTEGER", "description": "Age of the sailor.", "fields": []}]' what's a BigQuery query that answers the question 'Which boat has the most sailors?'
Gopher: SELECT boats.id AS boat_id, boats.name AS boat_name, COUNT(*) AS count FROM `sailors` JOIN `boats` ON sailors.boat_id = boats.id GROUP BY boats.id ORDER BY count DESC LIMIT 1"""
"""More preamble to get it thinking of writing SQL queries."""

CITIBIKE_PROMPT = f"""
{GOPHER_PROMPT_PREAMBLE}
{SQL_PREAMBLE}
User: Given the BigQuery table '{CITIBIKE_TRIPS_NAME}' with fields '{CITIBIKE_TRIPS_FIELDS}' and the table '{CITIBIKE_STATIONS_NAME}' with fields '{CITIBIKE_STATIONS_FIELDS}' what's a BigQuery query that answers the question '%s'
Gopher:"""

ENGINE = "code-davinci-002"


def question_to_code(question: str) -> str:
    prompt = CITIBIKE_PROMPT % question
    print("prompt:", prompt)
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Completion.create(
        engine=ENGINE,
        prompt=prompt,
        max_tokens=256,
        stop="User:",
        n=1,
    )
    completion = response.choices[0].text  # type: ignore
    print("completion:", completion)
    return completion
