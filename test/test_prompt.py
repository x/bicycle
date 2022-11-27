from typing import Optional

import pandas as pd

from bicycle.server import query_sqlite, question_to_code


def first_column_that_matches(
    df: pd.DataFrame, *substrs: str, but_not: Optional[str] = None
) -> Optional[pd.Series]:
    """Returns the first column that matches the first substr in substrs, case
    insensitive, or returns None."""
    for substr in substrs:
        for col in df.columns:
            if substr.lower() in col.lower():
                return col
    return None


def test_what_was_the_longest_trip_by_duration():
    """
    SELECT tripduration
    FROM trips
    ORDER BY tripduration
    DESC LIMIT 1;
    506344
    """
    question = "What was the longest trip by duration?"
    code = question_to_code(question)
    df = query_sqlite(code)
    col = first_column_that_matches(df, "duration", "time", "length", "seconds")

    assert len(df) == 1
    assert col is not None and col[0] == 506344


def test_which_station_had_the_most_rides_start_at_it():
    """
    SELECT station_id, name
    FROM stations
    JOIN (
      SELECT start_station_id AS station_id, count(*) AS start_count
      FROM stations
      JOIN trips
      ON stations.station_id = trips.start_station_id
      GROUP BY station_id
      ORDER BY start_count DESC
      LIMIT 1) AS most_starts
    USING (station_id) ;
    490|8 Ave & W 33 St
    """
    question = "Which station had the most rides start at it?"
    code = question_to_code(question)
    df = query_sqlite(code)
    col = first_column_that_matches(df, "station", "name")

    assert len(df) == 1
    assert col is not None and col[0] == "8 Ave & W 33 St"


def what_are_the_top_10_most_popular_stations():
    """
    SELECT station_id, name, start_count + end_count as usage
    FROM stations
    JOIN (
      SELECT start_station_id AS station_id, COUNT(*) AS start_count
      FROM trips
      GROUP BY start_station_id) starts
    USING (station_id)
    JOIN (
      SELECT end_station_id AS station_id, COUNT(*) AS end_count
      FROM trips
      GROUP BY end_station_id) ends
    USING (station_id)
    ORDER BY usage DESC
    LIMIT 10;
    497|E 17 St & Broadway|143
    293|Lafayette St & E 8 St|137
    435|W 21 St & 6 Ave|131
    426|West St & Chambers St|129
    368|Carmine St & 6 Ave|128
    490|8 Ave & W 33 St|128
    285|Broadway & E 14 St|117
    151|Cleveland Pl & Spring St|110
    284|Greenwich Ave & 8 Ave|107
    327|Vesey Pl & River Terrace|103
    """
    question = "What are the top 10 most popular stations?"
    code = question_to_code(question)
    df = query_sqlite(code)
    col = first_column_that_matches(df, "station", "name")

    assert len(df) == 10
    assert col is not None and "8 Ave & W 33 St" in col
