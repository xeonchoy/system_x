from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from auth import auth_bp
from database import db
from messages.sync_routes import sync_bp
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
import logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w')

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(sync_bp, url_prefix='/api/messages/sync')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/sync')
def whatsapp_sync():
    return render_template('sync.html')


@app.route('/api/contacts')
def get_contacts():
    try:
        contacts = db.get_contacts()
        return jsonify(contacts)
    except Exception as e:
        logging.error(f"Error fetching contacts: {e}")
        return jsonify({'error': 'Failed to fetch contacts'}), 500

@app.route('/api/messages/<int:contact_id>')
def get_messages(contact_id):
    try:
        messages = db.get_messages(contact_id)
        return jsonify(messages)
    except Exception as e:
        logging.error(f"Error fetching messages: {e}")
        return jsonify({'error': 'Failed to fetch messages'}), 500

@app.route('/api/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        db.send_message(message)
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({'error': 'Failed to send message'}), 500


@app.route('/api/messages/sync/status')
def sync_status():
    try:
        status = db.get_sync_status()
        return jsonify(status)
    except Exception as e:
        logging.error(f"Error getting sync status: {e}")
        return jsonify({'error': 'Failed to get sync status'}), 500

@app.route('/api/messages/sync/stop', methods=['POST'])
def api_stop_sync():
    try:
        db.stop_sync()
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error stopping sync: {e}")
        return jsonify({'error': 'Failed to stop sync'}), 500


if __name__ == '__main__':
    db.create_tables()  # Ensure tables are created before running
    app.run(debug=True)
