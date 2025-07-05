import pytest
from src.config_validator import ConfigValidator, ConfigValidationError, LearningMode


def test_valid_config_validation():
    """Test a valid configuration passes validation."""
    valid_config = {
        'learning_mode': 'SUPERVISED',
        'max_iterations': 100,
        'learning_rate': 0.01,
        'convergence_threshold': 0.001
    }
    
    result = ConfigValidator.validate_learning_config(valid_config)
    assert result == valid_config


def test_invalid_learning_mode():
    """Test that invalid learning modes raise an error."""
    invalid_configs = [
        {
            'learning_mode': 'INVALID_MODE',
            'max_iterations': 100,
            'learning_rate': 0.01,
            'convergence_threshold': 0.001
        },
        {
            'learning_mode': 123,
            'max_iterations': 100,
            'learning_rate': 0.01,
            'convergence_threshold': 0.001
        }
    ]
    
    for config in invalid_configs:
        with pytest.raises(ConfigValidationError, match="Invalid learning mode"):
            ConfigValidator.validate_learning_config(config)


def test_missing_required_keys():
    """Test that missing required keys raise an error."""
    incomplete_configs = [
        {},
        {'learning_mode': 'SUPERVISED'},
        {'max_iterations': 100}
    ]
    
    for config in incomplete_configs:
        with pytest.raises(ConfigValidationError, match="Missing required configuration key"):
            ConfigValidator.validate_learning_config(config)


def test_invalid_numeric_parameters():
    """Test various invalid numeric parameter scenarios."""
    invalid_configs = [
        {
            'learning_mode': 'SUPERVISED',
            'max_iterations': -1,
            'learning_rate': 0.01,
            'convergence_threshold': 0.001
        },
        {
            'learning_mode': 'SUPERVISED',
            'max_iterations': 100,
            'learning_rate': 1.1,
            'convergence_threshold': 0.001
        },
        {
            'learning_mode': 'SUPERVISED',
            'max_iterations': 100,
            'learning_rate': 0.01,
            'convergence_threshold': -0.1
        }
    ]
    
    for config in invalid_configs:
        with pytest.raises(ConfigValidationError):
            ConfigValidator.validate_learning_config(config)


def test_learning_mode_conversion():
    """Test conversion of learning mode strings and enums."""
    config_strings = [
        {
            'learning_mode': 'SUPERVISED',
            'max_iterations': 100,
            'learning_rate': 0.01,
            'convergence_threshold': 0.001
        },
        {
            'learning_mode': 'UNSUPERVISED',
            'max_iterations': 100,
            'learning_rate': 0.01,
            'convergence_threshold': 0.001
        },
        {
            'learning_mode': 'REINFORCEMENT',
            'max_iterations': 100,
            'learning_rate': 0.01,
            'convergence_threshold': 0.001
        }
    ]
    
    for config in config_strings:
        result = ConfigValidator.validate_learning_config(config)
        assert isinstance(result['learning_mode'], LearningMode)