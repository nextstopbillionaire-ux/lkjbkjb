from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.')
CORS(app)

DATA_FILE = 'server_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'resources': [], 'commonLinks': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/resources', methods=['POST'])
def add_resource():
    data = load_data()
    resource = request.json
    data['resources'].append(resource)
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    data = load_data()
    resource_data = request.json
    for i, r in enumerate(data['resources']):
        if r['id'] == resource_id:
            data['resources'][i] = resource_data
            save_data(data)
            return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.route('/api/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    data = load_data()
    data['resources'] = [r for r in data['resources'] if r['id'] != resource_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/quicklinks', methods=['POST'])
def add_quicklink():
    data = load_data()
    link = request.json
    data['commonLinks'].append(link)
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/quicklinks/<int:link_id>', methods=['DELETE'])
def delete_quicklink(link_id):
    data = load_data()
    data['commonLinks'] = [l for l in data['commonLinks'] if l['id'] != link_id]
    save_data(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
