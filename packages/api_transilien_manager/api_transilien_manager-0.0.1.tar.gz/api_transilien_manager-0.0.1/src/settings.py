import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR, "data")
gtfs_path = os.path.join(data_path, "gtfs-lines-last")

gtfs_csv_url = 'https://ressources.data.sncf.com/explore/dataset/sncf-transilien-gtfs/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true'


sqlite_path = os.path.join(BASE_DIR, "schedules.db")

# First doesn't work
# logs_path = "http://api-transilien-logs.s3-eu-west-1.amazonaws.com/logs/"
logs_path = os.path.join(BASE_DIR, "..", "logs")


# Mongo DB collections:
col_real_dep_unique = "real_departures_2"
