from ..env import CONFIG_FOLDER
import yaml

def get_csv_column_mapping():
    try:
        with open(f"{CONFIG_FOLDER}/csv.yml", "r") as file:
            config = yaml.safe_load(file)
        if not config:
            raise ValueError("Configuration file is empty or not found.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading the CSV configuration: {str(e)}")
    return config["columns"]

def get_key_rules():
    """
    Retrieve the configuration for a specific service.
    """
    try:
        print(CONFIG_FOLDER)
        with open(f"{CONFIG_FOLDER}/key_rules.yml", "r") as file:
            config = yaml.safe_load(file)
        if not config:
            raise ValueError("Configuration file is empty or not found.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading the key rules configuration")
    return config
