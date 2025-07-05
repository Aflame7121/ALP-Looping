import os
import json
import pytest
from src.config.config_manager import ConfigurationManager, ALPConfiguration, ConfigurationError

def test_default_configuration():
    """Test default configuration initialization."""
    config_manager = ConfigurationManager()
    config = config_manager.get_config()
    
    assert config.learning_rate == 0.01
    assert config.max_iterations == 100
    assert config.convergence_threshold == 1e-4
    assert config.logging_level == 'INFO'
    assert config.additional_params == {}

def test_file_configuration(tmp_path):
    """Test loading configuration from a JSON file."""
    config_file = tmp_path / "config.json"
    test_config = {
        "learning_rate": 0.05,
        "max_iterations": 200,
        "logging_level": "DEBUG"
    }
    
    with open(config_file, 'w') as f:
        json.dump(test_config, f)
    
    config_manager = ConfigurationManager(str(config_file))
    config = config_manager.get_config()
    
    assert config.learning_rate == 0.05
    assert config.max_iterations == 200
    assert config.logging_level == 'DEBUG'

def test_env_configuration(monkeypatch):
    """Test configuration from environment variables."""
    monkeypatch.setenv('ALP_LEARNING_RATE', '0.1')
    monkeypatch.setenv('ALP_MAX_ITERATIONS', '500')
    monkeypatch.setenv('ALP_ADDITIONAL_PARAMS', '{"key": "value"}')
    
    config_manager = ConfigurationManager()
    config = config_manager.get_config()
    
    assert config.learning_rate == 0.1
    assert config.max_iterations == 500
    assert config.additional_params == {"key": "value"}

def test_configuration_update():
    """Test updating configuration at runtime."""
    config_manager = ConfigurationManager()
    
    config_manager.update_config(
        learning_rate=0.02,
        logging_level='ERROR'
    )
    
    config = config_manager.get_config()
    
    assert config.learning_rate == 0.02
    assert config.logging_level == 'ERROR'

def test_save_and_load_configuration(tmp_path):
    """Test saving and loading configuration."""
    config_file = tmp_path / "saved_config.json"
    
    config_manager = ConfigurationManager()
    config_manager.update_config(
        learning_rate=0.03,
        max_iterations=150
    )
    
    config_manager.save_config(str(config_file))
    
    # Load saved configuration
    loaded_config_manager = ConfigurationManager(str(config_file))
    loaded_config = loaded_config_manager.get_config()
    
    assert loaded_config.learning_rate == 0.03
    assert loaded_config.max_iterations == 150

def test_configuration_error_handling(tmp_path):
    """Test error handling for invalid configurations."""
    # Invalid JSON file
    invalid_config_file = tmp_path / "invalid_config.json"
    with open(invalid_config_file, 'w') as f:
        f.write("{invalid json}")
    
    with pytest.raises(ConfigurationError):
        ConfigurationManager(str(invalid_config_file))
    
    # Invalid environment variable type
    with pytest.raises(ConfigurationError):
        os.environ['ALP_LEARNING_RATE'] = 'not a number'
        ConfigurationManager()