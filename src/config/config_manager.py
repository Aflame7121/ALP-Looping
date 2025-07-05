import os
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict, field
from copy import deepcopy

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

@dataclass
class ALPConfiguration:
    """
    Dataclass representing the configuration for the Adaptive Learning Process Loop.
    
    Attributes:
        learning_rate (float): Learning rate for the algorithm
        max_iterations (int): Maximum number of iterations
        convergence_threshold (float): Threshold for convergence detection
        logging_level (str): Logging verbosity level
        additional_params (Dict[str, Any]): Additional configuration parameters
    """
    learning_rate: float = 0.01
    max_iterations: int = 100
    convergence_threshold: float = 1e-4
    logging_level: str = 'INFO'
    additional_params: Dict[str, Any] = field(default_factory=dict)

class ConfigurationManager:
    """
    Manages loading, saving, and applying configuration parameters for the ALP Loop.
    
    Supports multiple configuration sources:
    - Default configuration
    - JSON file configuration
    - Environment variable configuration
    - Runtime configuration overrides
    """
    
    DEFAULT_CONFIG_PATH = 'config.json'
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ConfigurationManager.
        
        Args:
            config_path (Optional[str]): Path to the configuration file. 
                                         Uses default path if not provided.
        """
        self._config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config = self._load_configuration()
    
    def _load_configuration(self) -> ALPConfiguration:
        """
        Load configuration from multiple sources with precedence.
        
        Precedence order:
        1. Environment variables
        2. Configuration file
        3. Default configuration
        
        Returns:
            ALPConfiguration: Loaded and merged configuration
        """
        # Start with default configuration
        config = ALPConfiguration()
        
        # Try loading from JSON file
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r') as f:
                    file_config = json.load(f)
                    config = self._merge_configs(config, ALPConfiguration(**file_config))
        except (json.JSONDecodeError, IOError) as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
        
        # Override with environment variables
        env_config = self._load_env_config()
        config = self._merge_configs(config, env_config)
        
        return config
    
    def _load_env_config(self) -> ALPConfiguration:
        """
        Load configuration from environment variables.
        
        Returns:
            ALPConfiguration: Configuration loaded from environment variables
        """
        env_config_dict = {}
        for field_name, value in asdict(ALPConfiguration()).items():
            env_var = f'ALP_{field_name.upper()}'
            env_value = os.environ.get(env_var)
            
            if env_value is not None:
                try:
                    # Convert string to appropriate type
                    if field_name == 'additional_params':
                        env_config_dict[field_name] = json.loads(env_value)
                    elif isinstance(value, float):
                        env_config_dict[field_name] = float(env_value)
                    elif isinstance(value, int):
                        env_config_dict[field_name] = int(env_value)
                    else:
                        env_config_dict[field_name] = env_value
                except (ValueError, json.JSONDecodeError) as e:
                    raise ConfigurationError(f"Invalid environment variable {env_var}: {e}")
        
        return ALPConfiguration(**env_config_dict)
    
    def _merge_configs(self, base_config: ALPConfiguration, 
                       override_config: ALPConfiguration) -> ALPConfiguration:
        """
        Merge two configurations with the override taking precedence.
        
        Args:
            base_config (ALPConfiguration): Base configuration
            override_config (ALPConfiguration): Configuration to override base
        
        Returns:
            ALPConfiguration: Merged configuration
        """
        merged_config = deepcopy(base_config)
        
        for field_name, value in asdict(override_config).items():
            if value is not None:
                setattr(merged_config, field_name, value)
        
        return merged_config
    
    def get_config(self) -> ALPConfiguration:
        """
        Get the current configuration.
        
        Returns:
            ALPConfiguration: Current configuration
        """
        return deepcopy(self._config)
    
    def update_config(self, **kwargs) -> None:
        """
        Update configuration with provided parameters.
        
        Args:
            **kwargs: Configuration parameters to update
        
        Raises:
            ConfigurationError: If invalid configuration parameters are provided
        """
        try:
            update_config = ALPConfiguration(**kwargs)
            self._config = self._merge_configs(self._config, update_config)
        except TypeError as e:
            raise ConfigurationError(f"Invalid configuration update: {e}")
    
    def save_config(self, path: Optional[str] = None) -> None:
        """
        Save current configuration to a JSON file.
        
        Args:
            path (Optional[str]): Path to save configuration. 
                                  Uses default path if not provided.
        """
        save_path = path or self._config_path
        with open(save_path, 'w') as f:
            json.dump(asdict(self._config), f, indent=4)