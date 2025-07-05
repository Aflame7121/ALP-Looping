from flask import Flask, request, jsonify
from src.config_model import alp_config

app = Flask(__name__)

@app.route('/config', methods=['GET'])
def get_config():
    """
    Retrieve current ALP configuration
    
    Returns:
        JSON response with current configuration
    """
    try:
        return jsonify(alp_config.get_config()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/config', methods=['PUT'])
def update_config():
    """
    Update ALP configuration
    
    Expects JSON payload with configuration parameters
    
    Returns:
        JSON response with updated configuration or error message
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    try:
        new_config = request.get_json()
        updated_config = alp_config.update_config(new_config)
        return jsonify(updated_config), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)