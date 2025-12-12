from flask import Flask, request, jsonify
from datetime import datetime
from validator import MeetingValidator

app = Flask(__name__)
validator = MeetingValidator()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/validate', methods=['POST'])
def validate():
    try:
        result = validator.validate(request.json)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
