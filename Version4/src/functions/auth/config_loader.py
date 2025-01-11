import json
import logging
from typing import Dict, Any

logger = logging.getLogger("config_logger")


class ConfigLoaderError(Exception):
    """
    Custom Exception for configuration loading errors.
    """
    def __init__(self, message: str):
        super().__init__(message)


def load_config(file_path: str) -> Dict[str, Any]:
    """
    Loads a configuration file in JSON format.
    """
    try:
        logger.info(f"Loading configuration from {file_path}")
        with open(file_path, "r") as file:
            config = json.load(file)
            logger.info(f"Configuration loaded successfully: {file_path}")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        raise ConfigLoaderError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError as json_err:
        logger.error(f"Error decoding JSON from {file_path}: {json_err}")
        raise ConfigLoaderError(f"Invalid JSON in configuration file: {file_path}")
    except Exception as ex:
        logger.error(f"Unexpected error loading configuration: {ex}")
        raise ConfigLoaderError(f"Unexpected error: {ex}")
