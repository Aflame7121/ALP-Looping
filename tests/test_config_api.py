import pytest
from flask import json
from src.config_api import app
from src.config_model import ALPConfigSchema

@pytest.fixture
def client():
    """
    Create test client for Flask app
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_config(client):
    """
    Test retrieving default configuration
    """
    response = client.get('/config')
    assert response.status_code == 200
    config_data = json.loads(response.data)
    
    schema = ALPConfigSchema()
    try:
        schema.load(config_data)
    except Exception as e:
        pytest.fail(f"Configuration does not match schema: {str(e)}")

def test_update_config_valid(client):
    """
    Test updating configuration with valid parameters
    """
    new_config = {
        "learning_rate": 0.1,
        "max_iterations": 5000,
        "convergence_threshold": 0.0005,
        "debug_mode": True
    }
    
    response = client.put('/config', json=new_config)
    assert response.status_code == 200
    
    updated_config = json.loads(response.data)
    assert updated_config['learning_rate'] == 0.1
    assert updated_config['max_iterations'] == 5000

def test_update_config_invalid(client):
    """
    Test updating configuration with invalid parameters
    """
    invalid_configs = [
        {"learning_rate": 2.0},  # Out of range
        {"max_iterations": -1},  # Negative value
        {"convergence_threshold": "not_a_number"}  # Wrong type
    ]
    
    for invalid_config in invalid_configs:
        response = client.put('/config', json=invalid_config)
        assert response.status_code == 400