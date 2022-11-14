CITIBIKE_STATIONS_NAME = "bigquery-public-data.new_york.citibike_stations"
CITIBIKE_STATIONS_FIELDS = [
    {
        "name": "station_id",
        "mode": "REQUIRED",
        "type": "INTEGER",
        "description": "Unique identifier of a station.",
        "fields": [],
    },
    {
        "name": "name",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "Public name of the station.",
        "fields": [],
    },
    {
        "name": "short_name",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "Short name or other type of identifier, as used by the data publisher.",
        "fields": [],
    },
    {
        "name": "latitude",
        "mode": "NULLABLE",
        "type": "FLOAT",
        "description": "The latitude of station. The field value must be a valid WGS 84 latitude in decimal degrees format.",
        "fields": [],
    },
    {
        "name": "longitude",
        "mode": "NULLABLE",
        "type": "FLOAT",
        "description": "The longitude of station. The field value must be a valid WGS 84 latitude in decimal degrees format.",
        "fields": [],
    },
    {
        "name": "region_id",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "ID of the region where station is located.",
        "fields": [],
    },
    {
        "name": "rental_methods",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "Array of enumerables containing the payment methods accepted at this station.",
        "fields": [],
    },
    {
        "name": "capacity",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "ANumber of total docking points installed at this station, both available and unavailable.",
        "fields": [],
    },
    {
        "name": "eightd_has_key_dispenser",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "",
        "fields": [],
    },
    {
        "name": "num_bikes_available",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Number of bikes available for rental.",
        "fields": [],
    },
    {
        "name": "num_bikes_disabled",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Number of disabled bikes at the station.",
        "fields": [],
    },
    {
        "name": "num_docks_available",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Number of docks accepting bike returns.",
        "fields": [],
    },
    {
        "name": "num_docks_disabled",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Number of empty but disabled dock points at the station.",
        "fields": [],
    },
    {
        "name": "is_installed",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "Is the station currently on the street?",
        "fields": [],
    },
    {
        "name": "is_renting",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "Is the station currently renting bikes?",
        "fields": [],
    },
    {
        "name": "is_returning",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "Is the station accepting bike returns?",
        "fields": [],
    },
    {
        "name": "eightd_has_available_keys",
        "mode": "NULLABLE",
        "type": "BOOLEAN",
        "description": "",
        "fields": [],
    },
    {
        "name": "last_reported",
        "mode": "NULLABLE",
        "type": "TIMESTAMP",
        "description": "Timestamp indicating the last time this station reported its status to the backend, in NYC local time.",
        "fields": [],
    },
]

CITIBIKE_TRIPS_NAME = "bigquery-public-data.new_york.citibike_trips"
CITIBIKE_TRIPS_FIELDS = [
    {
        "name": "tripduration",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Trip Duration (in seconds)",
        "fields": [],
    },
    {
        "name": "starttime",
        "mode": "NULLABLE",
        "type": "TIMESTAMP",
        "description": "Start Time",
        "fields": [],
    },
    {
        "name": "stoptime",
        "mode": "NULLABLE",
        "type": "TIMESTAMP",
        "description": "Stop Time",
        "fields": [],
    },
    {
        "name": "start_station_id",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Start Station ID",
        "fields": [],
    },
    {
        "name": "start_station_name",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "Start Station Name",
        "fields": [],
    },
    {
        "name": "start_station_latitude",
        "mode": "NULLABLE",
        "type": "FLOAT",
        "description": "Start Station Latitude",
        "fields": [],
    },
    {
        "name": "start_station_longitude",
        "mode": "NULLABLE",
        "type": "FLOAT",
        "description": "Start Station Longitude",
        "fields": [],
    },
    {
        "name": "end_station_id",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "End Station ID",
        "fields": [],
    },
    {
        "name": "end_station_name",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "End Station Name",
        "fields": [],
    },
    {
        "name": "end_station_latitude",
        "mode": "NULLABLE",
        "type": "FLOAT",
        "description": "End Station Latitude",
        "fields": [],
    },
    {
        "name": "end_station_longitude",
        "mode": "NULLABLE",
        "type": "FLOAT",
        "description": "End Station Longitude",
        "fields": [],
    },
    {
        "name": "bikeid",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Bike ID",
        "fields": [],
    },
    {
        "name": "usertype",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "User Type (Customer = 24-hour pass or 7-day pass user, Subscriber = Annual Member)",
        "fields": [],
    },
    {
        "name": "birth_year",
        "mode": "NULLABLE",
        "type": "INTEGER",
        "description": "Year of Birth",
        "fields": [],
    },
    {
        "name": "gender",
        "mode": "NULLABLE",
        "type": "STRING",
        "description": "Gender (unknown, male, female)",
        "fields": [],
    },
]
