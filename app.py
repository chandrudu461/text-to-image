from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    api_url = 'https://api.limewire.com/api/image/generation'
    api_key = 'lmwr_sk_nXHv4FgLWI_AMu0bXsnlUJ0UMMvbRwiLbVtHCq4pN9pD9rTQ'  # Replace with your LimeWire API key

    headers = {
        'Content-Type': 'application/json',
        'X-Api-Version': 'v1',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    payload = {
        'prompt': prompt,
        'aspect_ratio': '1:1'
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        response_data = response.json()
        
        # Log the response data to inspect its structure
        print(response_data)

        if 'data' in response_data and len(response_data['data']) > 0:
            image_url = response_data['data'][0]['asset_url']
            return jsonify({'imageUrl': image_url})
        else:
            return jsonify({'error': 'No images found in the response'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
