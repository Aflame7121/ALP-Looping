from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum, auto


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass


class LearningMode(Enum):
    SUPERVISED = auto()
    UNSUPERVISED = auto()
    REINFORCEMENT = auto()


@dataclass
class ConfigValidator:
    """
    Configuration validator for Adaptive Learning Process (ALP) parameters.
    
    Validates configuration parameters to ensure they meet system requirements
    and constraints before being applied to the learning process.
    """

    @staticmethod
    def validate_learning_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the overall learning configuration.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary to validate
        
        Returns:
            Dict[str, Any]: Validated configuration
        
        Raises:
            ConfigValidationError: If configuration is invalid
        """
        # Validate required keys
        required_keys = [
            'learning_mode', 
            'max_iterations', 
            'learning_rate', 
            'convergence_threshold'
        ]
        
        for key in required_keys:
            if key not in config:
                raise ConfigValidationError(f"Missing required configuration key: {key}")
        
        # Validate learning mode first
        config['learning_mode'] = ConfigValidator._validate_learning_mode(config.get('learning_mode'))
        
        # Validate numeric parameters
        ConfigValidator._validate_numeric_config(config)
        
        return config
    
    @staticmethod
    def _validate_learning_mode(mode: Union[str, LearningMode]) -> LearningMode:
        """
        Validate and convert learning mode.
        
        Args:
            mode (Union[str, LearningMode]): Learning mode to validate
        
        Returns:
            LearningMode: Validated learning mode
        
        Raises:
            ConfigValidationError: If mode is invalid
        """
        try:
            if isinstance(mode, str):
                return LearningMode[mode.upper()]
            elif isinstance(mode, LearningMode):
                return mode
            else:
                raise ValueError("Invalid learning mode type")
        except (KeyError, ValueError):
            raise ConfigValidationError(
                f"Invalid learning mode. Must be one of {[m.name for m in LearningMode]}"
            )
    
    @staticmethod
    def _validate_numeric_config(config: Dict[str, Any]) -> None:
        """
        Validate numeric configuration parameters.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        
        Raises:
            ConfigValidationError: If numeric parameters are invalid
        """
        numeric_validations = {
            'max_iterations': (lambda x: x > 0, "Must be a positive integer"),
            'learning_rate': (lambda x: 0 < x <= 1, "Must be between 0 and 1"),
            'convergence_threshold': (lambda x: 0 < x < 1, "Must be between 0 and 1")
        }
        
        for param, (validator, error_msg) in numeric_validations.items():
            value = config.get(param)
            
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                raise ConfigValidationError(f"{param} must be a numeric value")
            
            if not validator(numeric_value):
                raise ConfigValidationError(f"{param} {error_msg}")