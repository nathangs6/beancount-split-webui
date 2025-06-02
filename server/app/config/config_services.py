from ..env import CONFIG_FOLDER
import yaml

class ConfigServices:
    def get_key_rules(self):
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
        print(config)
        return config
