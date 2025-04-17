from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'environment': os.getenv('ENV', 'development')
    })

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from the sample deployment app!',
        'environment': os.getenv('ENV', 'development')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 