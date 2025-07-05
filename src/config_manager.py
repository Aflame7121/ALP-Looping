from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ValidationError
import json
import os

class ALPLoopConfig(BaseModel):
    """
    Configuration model for Adaptive Learning Process (ALP) Loop
    Defines core parameters with validation and defaults
    """
    max_iterations: int = Field(default=100, gt=0, description="Maximum number of learning iterations")
    learning_rate: float = Field(default=0.01, gt=0, le=1, description="Learning rate for model updates")
    early_stopping_threshold: float = Field(default=0.001, gt=0, description="Threshold for early stopping")
    random_seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")
    verbose: bool = Field(default=False, description="Enable verbose logging")

class ConfigurationManager:
    """
    Manages loading, saving, and applying ALP loop configuration parameters
    Provides a clean interface for configuration interactions
    """
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        :param config_path: Optional path to configuration file
        """
        self._config_path = config_path or 'alp_config.json'
        self._config = self._load_config()

    def _load_config(self, config_data: Optional[Dict[str, Any]] = None) -> ALPLoopConfig:
        """
        Load configuration from file or return default configuration
        
        :param config_data: Optional configuration dictionary to override file/default config
        :return: Validated ALPLoopConfig
        :raises FileNotFoundError: If config file is not found
        :raises ValidationError: If configuration is invalid
        """
        try:
            if config_data:
                return ALPLoopConfig(**config_data)
            
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r') as f:
                    file_config_data = json.load(f)
                return ALPLoopConfig(**file_config_data)
            
            return ALPLoopConfig()
        except FileNotFoundError:
            return ALPLoopConfig()
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e}")

    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """
        Save configuration to file
        
        :param config: Optional configuration dictionary to override current config
        :raises ValidationError: If provided configuration is invalid
        """
        try:
            if config:
                self._config = ALPLoopConfig(**config)
            
            with open(self._config_path, 'w') as f:
                json.dump(self._config.model_dump(), f, indent=2)
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e}")

    def get_config(self) -> ALPLoopConfig:
        """
        Retrieve current configuration
        
        :return: Current ALPLoopConfig
        """
        return self._config

    def update_config(self, **kwargs):
        """
        Update specific configuration parameters
        
        :param kwargs: Configuration parameters to update
        :raises ValidationError: If any parameter is invalid
        """
        try:
            updated_config = self._config.model_dump()
            updated_config.update(kwargs)
            self._config = ALPLoopConfig(**updated_config)
            self.save_config()
        except ValidationError as e:
            raise ValueError(f"Invalid configuration update: {e}")