from ..env import USERS
import yaml

def get_csv_column_mapping(owner: str):
    try:
        if owner not in USERS:
            raise ValueError(f"Invalid owner: {owner}.")
        config_folder = USERS[owner]["beancount_folder"]
        print(config_folder)
        with open(f"{config_folder}/csv.yml", "r") as file:
            config = yaml.safe_load(file)
        if not config:
            raise ValueError("Configuration file is empty or not found.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading the CSV configuration: {str(e)}")
    return config["columns"]

def get_key_rules(owner: str):
    """
    Retrieve the configuration for a specific service.
    """
    try:
        if owner not in USERS:
            raise ValueError(f"Invalid owner: {owner}.")
        config_folder = USERS[owner]["beancount_folder"]
        with open(f"{config_folder}/key_rules.yml", "r") as file:
            config = yaml.safe_load(file)
        if not config:
            raise ValueError("Configuration file is empty or not found.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading the key rules configuration")
    return config
