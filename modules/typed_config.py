"""
A typed configuration class that loads a .conf file, exposes keys as attributes,
and supports setting values with type validation.
@author Abracadaniel22
"""
import configparser
from typing import Any, Dict, Type, Union

class TypedConfig:
    def __init__(self, config_file: str, schema: Dict[str, Type[Union[str, int, float, bool]]], section: str = 'config'):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)
        self._section = section
        self._schema = schema
        self._config_file = config_file

    def __getattr__(self, name: str) -> Any:
        if name not in self._schema:
            raise AttributeError(f"Configuration key '{name}' not defined in schema for {self._config_file}")
        
        if not self._config.has_option(self._section, name):
            return None
        
        value = self._config.get(self._section, name)
        
        try:
            target_type = self._schema[name]
            if target_type == bool:
                return self._config.getboolean(self._section, name)
            elif target_type == int:
                return self._config.getint(self._section, name)
            elif target_type == float:
                return self._config.getfloat(self._section, name)
            elif target_type == str:
                return value
        except ValueError as e:
            raise ValueError(f"Invalid value for '{name}': {str(e)}")
        
        raise TypeError(f"Unsupported type for key '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting internal attributes starting with '_'
        if name.startswith('_'):
            super().__setattr__(name, value)
            return
        
        if name not in self._schema:
            raise AttributeError(f"Configuration key '{name}' not defined in schema")
        
        expected_type = self._schema[name]
        if not isinstance(value, expected_type):
            try:
                if expected_type == bool:
                    if isinstance(value, str):
                        value = value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        value = bool(value)
                elif expected_type == int:
                    value = int(value)
                elif expected_type == float:
                    value = float(value)
                elif expected_type == str:
                    value = str(value)
            except (ValueError, TypeError):
                raise TypeError(f"Value for '{name}' must be of type {expected_type.__name__}")
        
        if self._section not in self._config:
            self._config[self._section] = {}
        
        self._config.set(self._section, name, str(value))
        with open(self._config_file, 'w') as f:
            self._config.write(f)