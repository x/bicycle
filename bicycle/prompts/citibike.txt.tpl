________
User: Given the SQLite Table:
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
User: Given the SQLite Table:
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
User: Which two stations are the furthest apart?
________
$bot_name:
SELECT start_station.name as end_station, end_station.name AS end_station, SQRT(POW(start_station.latitude - end_station.latitude, 2) + POW(start_station.longitude - end_station.longitude, 2)) AS distance
FROM stations AS start_station
JOIN stations AS end_station
WHERE start_station.station_id != end_station.station_id
ORDER BY distance DESC
LIMIT 1;
________
User: What was the longest trip?
________
$bot_name:
SELECT *
FROM trips
ORDER BY tripduration DESC
LIMIT 1;
________
User: How many trips were started with fewer than 10 nikes available?
________
$bot_name:
SELECT COUNT(*) as num_trips
FROM trips
JOIN stations
ON trips.start_station_id = trips.start_station_id
WHERE num_bikes_available < 10
________
User: What were the top 10 fastest trips;
________
$bot_name:
SELECT trips.*, SQRT(POW(start_station_latitude - end_station_latitude, 2) + POW(start_station_longitude - end_station_longitude, 2)) / tripduration AS speed
FROM trips
ORDER BY speed DESC
LIMIT 10;
________
User: $question;
________
$bot_name:
"""