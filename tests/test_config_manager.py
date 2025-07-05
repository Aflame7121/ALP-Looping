import os
import pytest
from src.config_manager import ConfigurationManager, ALPLoopConfig

@pytest.fixture
def temp_config_path(tmp_path):
    """Fixture to generate a temporary config file path"""
    return str(tmp_path / "test_config.json")

def test_default_configuration():
    """Test default configuration creation"""
    config_manager = ConfigurationManager()
    config = config_manager.get_config()
    
    assert config.max_iterations == 100
    assert config.learning_rate == 0.01
    assert config.early_stopping_threshold == 0.001
    assert config.random_seed is None
    assert config.verbose is False

def test_save_and_load_configuration(temp_config_path):
    """Test saving and loading configuration"""
    config_manager = ConfigurationManager(config_path=temp_config_path)
    config_manager.save_config({
        "max_iterations": 50,
        "learning_rate": 0.005,
        "verbose": True
    })

    # Reload configuration
    reloaded_manager = ConfigurationManager(config_path=temp_config_path)
    config = reloaded_manager.get_config()

    assert config.max_iterations == 50
    assert config.learning_rate == 0.005
    assert config.verbose is True

def test_update_configuration(temp_config_path):
    """Test updating configuration parameters"""
    config_manager = ConfigurationManager(config_path=temp_config_path)
    config_manager.update_config(max_iterations=75, learning_rate=0.02)

    updated_config = config_manager.get_config()
    assert updated_config.max_iterations == 75
    assert updated_config.learning_rate == 0.02

def test_invalid_configuration_validation():
    """Test validation of configuration parameters"""
    with pytest.raises(ValueError):
        ConfigurationManager()._load_config({
            "max_iterations": -10,  # Invalid: should be positive
            "learning_rate": 2.0    # Invalid: should be <= 1
        })

def test_update_with_invalid_parameters(temp_config_path):
    """Test updating configuration with invalid parameters"""
    config_manager = ConfigurationManager(config_path=temp_config_path)
    
    with pytest.raises(ValueError):
        config_manager.update_config(max_iterations=-10)
    
    with pytest.raises(ValueError):
        config_manager.update_config(learning_rate=2.0)