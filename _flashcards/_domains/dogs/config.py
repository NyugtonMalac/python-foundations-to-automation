import os

DOGS_DOMAIN_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(DOGS_DOMAIN_DIR, "data_private", "users.json")
SAVES_DIR = os.path.join(DOGS_DOMAIN_DIR, "saves")


DATA_DIR = os.path.join(DOGS_DOMAIN_DIR, "data")
DOGS_JSON_PATH = os.path.join(DATA_DIR, "dogs.json") 

RAW_DATA_INPUT_DIR = os.path.join(DOGS_DOMAIN_DIR, "raw_data_inputs")
DOGS_CSV_PATH = os.path.join(RAW_DATA_INPUT_DIR, "dogs.csv")
RENAME_MAP_PATH = os.path.join(RAW_DATA_INPUT_DIR, "rename_map.json")

STATIC_IMG_DIR = os.path.join(DOGS_DOMAIN_DIR, "static", "img")