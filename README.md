# Setup

The expected dev platform is an Apple Silicon Mac.

Binaries are managed via Homebrew (a mix of native and rosetta).

Python version is managed by `pyenv`, the virtual env is created by `poetry`,
and they're linked using `pyenv-virtualenv`. For the most part, you should just
be able to run `make setup` and have stuff *just work*™️. For now, the python
version is built and run under rosetta (hence rosetta Homebrew packages).

# Dev

To dev locally setup a `.env` with the environment variables:

```.env
OPENAI_API_KEY=...
```

To start the server run `make up` and navigate to 127.0.0.1:5000 This runs flask
in debug mode with hot-code reloading for most changes.

`black`, `isort`, `flake8`, and `mypy` are all installed by poetry.

These poetry-managed versions are pointed to for VSCode in the
`.vscode/settings.json` and things should *just world*™️ if VSCode is opened at
the root of this project.

Alternatively, `make lint` and `make format`.

# How I Created the SQLite Tables

1. I went to the public BigQuery dataset and copied the fields from both tables
   in `CREATE TABLE` statement format and reformatted them to look like SQLite
   tables like so...

   ```
   CREATE TABLE trips(
     tripduration            INT,  -- Trip Duration (in seconds)
     starttime               TEXT, -- Start Time, in NYC local time.
     stoptime                TEXT, -- Stop Time, in NYC local time.
     start_station_id        INT,  -- Start Station ID
     start_station_name      TEXT, -- Start Station Name
     start_station_latitude  NUM,  -- Start Station Latitude
     start_station_longitude NUM,  -- Start Station Longitude
     end_station_id          INT,  -- End Station ID
     end_station_name        TEXT, -- End Station Name
     end_station_latitude    NUM,  -- End Station Latitude
     end_station_longitude   NUM,  -- End Station Longitude
     bikeid                  INT,  -- Bike ID
     usertype                TEXT, -- User Type (Customer = 24-hour pass or 7-day pass user, Subscriber = Annual Member)
     birth_year              INT,  -- Year of Birth
     gender                  TEXT, -- Gender (unknown, male, female)
     customer_plan           TEXT  -- The name of the plan that determines the rate charged for the trip
   );


   CREATE TABLE stations(
     station_id                INT,  -- Unique identifier of a station.
     name                      TEXT, -- Public name of the station.
     short_name                TEXT, -- Short name or other type of identifier, as used by the data publisher.
     latitude                  NUM,  -- The latitude of station. The field value must be a valid WGS 84 latitude in decimal degrees format.
     longitude                 NUM,  -- The longitude of station. The field value must be a valid WGS 84 longitude in decimal degrees format.
     region_id                 INT,  -- ID of the region where station is located.
     rental_methods            TEXT, -- Array of enumerables containing the payment methods accepted at this station.
     capacity                  INT,  -- ANumber of total docking points installed at this station, both available and unavailable.
     eightd_has_key_dispenser  INT,  -- Is the station equipped with a key dispenser
     num_bikes_available       INT,  -- Number of bikes available for rental.
     num_bikes_disabled        INT,  -- Number of disabled bikes at the station.
     num_docks_available       INT,  -- Number of docks accepting bike returns.
     num_docks_disabled        INT,  -- Number of empty but disabled dock points at the station.
     is_installed              INT,  -- Is the station currently on the street?
     is_renting                INT,  -- Is the station currently renting bikes?
     is_returning              INT,  -- Is the station accepting bike returns?
     eightd_has_available_keys INT,  -- Is the station capable of dispensing keys
     last_reported             TEXT -- Timestamp indicating the last time this station reported its status to the backend, in NYC local time.
   );
   ```
   And used these to create the tables in the db file.

2. I exported the datasets to CSV files and downloaded them. For samples of the
   trips I did...
   ```sql
   SELECT *
   FROM trips
   WHERE tripduration IS NOT NULL -- There's bad data for some reason
   ORDER BY RAND() LIMIT 10000`
   ```
3. **I removed the headers from the csvs** and then
   loaded them into SQLite using...
   ```
   .create csv
   .import trips.csv trips
   .import stations.csv stations
   ```
4. IIRC there were some null rows in the stations table I had to prune out as
   well.