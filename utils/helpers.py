
import os
import json
from typing import Dict, Any

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If the configuration file is not valid JSON.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as config_file:
        try:
            config = json.load(config_file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in configuration file: {config_path}", e.doc, e.pos)

    return config

def create_directory(directory_path: str) -> None:
    """
    Create a directory if it doesn't exist.

    Args:
        directory_path (str): Path to the directory to be created.
    """
    os.makedirs(directory_path, exist_ok=True)

def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: File extension (without the dot).
    """
    return os.path.splitext(file_path)[1][1:]
