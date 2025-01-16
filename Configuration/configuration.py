import configparser
import os
import pandas as pd


def load_config(file_path):
    """
    Loads configuration settings from a specified .ini file.
    Returns a dictionary of settings.
    """
    config = configparser.ConfigParser()

    try:
        config.read(file_path)
        if not config.sections():
            raise FileNotFoundError(f"Config file is empty or not found: {file_path}")
        settings = {
            'server': config.get('settings', 'server'),
            'database': config.get('settings', 'database'),
            'username': config.get('settings', 'username'),
            'password': config.get('settings', 'password'),
            'driver': config.get('settings', 'driver'),
        }
        print(f"Settings loaded from {file_path}: ", settings)
        return settings
    except configparser.Error as e:
        raise configparser.Error(f"Failed to load config file: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid input in config file: {e}")


def load_user_config():
    """
    Tries to load the user configuration from UserConfig.ini.
    If not found or invalid, falls back to loading the default configuration.
    """
    user_config_path = 'UserConfig.ini'

    if os.path.exists(user_config_path):
        try:
            # Attempt to load the user configuration
            print(f"Attempting to load UserConfig.ini from {user_config_path}...")
            return load_config(user_config_path)
        except Exception as e:
            print(f"Error reading UserConfig.ini: {e}")
            print("UserConfig.ini loading failed. Falling back to DefaultConfig.ini.")
            return None  # Explicitly return None if user config fails
    else:
        print("UserConfig.ini does not exist. Falling back to DefaultConfig.ini.")
        return None  # Return None if user config doesn't exist


def load_default_config():
    """
    Loads the default configuration from DefaultConfigs.ini.
    """
    default_config_path = 'DefaultConfig.ini'
    print(f"Falling back to default settings from {default_config_path}...")
    return load_config(default_config_path)


def get_final_config(user_config, default_config):
    """
    Combines user and default configuration settings.
    If a setting is missing in the user config, it falls back to the default config.
    """
    final_config = {}
    default_settings = default_config

    required_keys = ['server', 'database', 'username', 'password', 'driver']

    for key in required_keys:
        # Use user-config value if available, otherwise fallback to default
        final_config[key] = user_config.get(key) or default_settings.get(key)

        if final_config[key] is None:
            raise KeyError(f"Required config key: {key} is missing in both user and default configs.")
    return final_config


def load_csv_paths_from_config():
    """
    Load the CSV file paths from the configuration.
    """
    config = load_user_config()

    if not config:
        print("No user config found, using default config.")
        config = load_default_config()

    csv_paths = {
        'authors_csv_path': config.get('CSV', 'authors_csv_path', fallback=None),
        'genres_csv_path': config.get('CSV', 'genres_csv_path', fallback=None)
    }

    if not csv_paths['authors_csv_path'] or not os.path.exists(csv_paths['authors_csv_path']):
        print(f"Warning: Authors CSV file path {csv_paths['authors_csv_path']} is invalid.")
    if not csv_paths['genres_csv_path'] or not os.path.exists(csv_paths['genres_csv_path']):
        print(f"Warning: Genres CSV file path {csv_paths['genres_csv_path']} is invalid.")

    return csv_paths


def load_from_csv(file_path):
    """
    Load data from a CSV file and return as a DataFrame.
    """
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path)
            print(f"Data successfully loaded from {file_path}")
            return data
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None
    else:
        print(f"CSV file not found at path: {file_path}")
        return None
