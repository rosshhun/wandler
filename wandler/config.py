import yaml
from pathlib import Path
from typing import Optional
from pydantic import ValidationError
from .models import Config
from .errors import ConfigError

class ConfigManager:
    def __init__(self):
        self._config_cache: Optional[Config] = None
        self._config_path: Optional[Config] = None

    def find_config_file(self) -> Optional[Path]:
        """
        Search for wandler config files in current and parent directories.

        Returns:
            Path: Path to config file if found, otherwise None.
        """
        config_files = ('wandler.yml', '.wandler.yml', 'wandler.yaml', '.wandler.yaml',
                        'Wandler.yaml', '.Wandler.yaml', 'Wandler.yml', '.Wandler.yml')
        for path in (Path.cwd(), *Path.cwd().parents):
            for filename in config_files:
                file_path = path / filename
                if file_path.exists():
                    self._config_path = file_path
                    return file_path
        return None

    def load_and_validate(self, config_path: Path) -> Config:
        """
        Load and validate the configuration from the given YAML file path.

        Args:
            config_path (Path): The path to the configuration file.

        Returns:
            Config: The validated configuration object.

        Raises:
            ConfigError: If the file cannot be read, is invalid YAML, or fails validation.
        """
        try:
            raw_text = config_path.read_text()
            raw_data = yaml.safe_load(raw_text)
            return Config.model_validate(raw_data)
        except OSError as e:
            raise ConfigError(f"Error reading file {config_path}: {e}") from e
        except yaml.YAMLError as e:
            raise ConfigError(f"Error: '{config_path}' is not valid YAML. {e}") from e
        except ValidationError as e:
            raise ConfigError(f"Error: '{config_path}' has invalid content. {e}") from e

    def get_config_path(self):
        """
        Get the path to the configuration file, searching if not already cached.

        Returns:
            Path: The path to the configuration file.

        Raises:
            ConfigError: If no configuration file is found.
        """
        if self._config_path:
            return self._config_path

        path = self.find_config_file()
        if path is None:
            raise ConfigError("Error: No wandler.yaml configuration file found.")
        self._config_path = path
        return path

    def get_config(self) -> Config:
        """
        Get the configuration object, loading and validating if not already cached.

        Returns:
            Config: The configuration object.
        """
        if self._config_cache:
            return self._config_cache

        config_path = self.get_config_path()
        self._config_cache = self.load_and_validate(config_path)
        return self._config_cache