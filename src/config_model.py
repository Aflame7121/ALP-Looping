from typing import Dict, Any
from marshmallow import Schema, fields, validate

class ALPConfigSchema(Schema):
    """
    Schema for Adaptive Learning Process (ALP) Configuration
    Validates and serializes configuration parameters
    """
    learning_rate = fields.Float(
        required=True, 
        validate=validate.Range(min=0.0, max=1.0)
    )
    max_iterations = fields.Integer(
        required=True, 
        validate=validate.Range(min=1, max=10000)
    )
    convergence_threshold = fields.Float(
        required=True, 
        validate=validate.Range(min=0.0, max=1.0)
    )
    debug_mode = fields.Boolean(
        required=False, 
        default=False
    )

class ALPConfig:
    """
    Configuration management class for Adaptive Learning Process
    Provides methods to validate, retrieve, and update configuration
    """
    def __init__(self):
        self._config = {
            "learning_rate": 0.01,
            "max_iterations": 1000,
            "convergence_threshold": 0.001,
            "debug_mode": False
        }
        self._schema = ALPConfigSchema()

    def get_config(self) -> Dict[str, Any]:
        """
        Retrieve current configuration
        
        Returns:
            Dict[str, Any]: Current configuration parameters
        """
        return self._config.copy()

    def update_config(self, new_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update configuration with validation
        
        Args:
            new_config (Dict[str, Any]): New configuration parameters
        
        Returns:
            Dict[str, Any]: Updated configuration after validation
        
        Raises:
            ValueError: If configuration validation fails
        """
        try:
            validated_config = self._schema.load(new_config)
            self._config.update(validated_config)
            return self._config
        except Exception as e:
            raise ValueError(f"Invalid configuration: {str(e)}")

# Global configuration instance
alp_config = ALPConfig()