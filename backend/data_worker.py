from flask import Flask, jsonify
from flask_cors import CORS
import socketio
import eventlet
import fastf1

# Initialize
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
app = Flask(__name__)
CORS(app)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({"status": "live", "service": "f1-backend"})

# WebSocket events
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")
    sio.emit('acknowledge', {'data': 'Connected to F1 WS'}, room=sid)

def emit_f1_data():
    session = fastf1.get_session(2023, 'Spain', 'Q')
    session.load()
    
    while True:
        try:
            lap_data = session.laps.to_dict('records')
            sio.emit('f1_update', lap_data[:20])
            eventlet.sleep(1)
        except Exception as e:
            print(f"Data error: {str(e)}")

if __name__ == '__main__':
    eventlet.spawn(emit_f1_data)
    eventlet.wsgi.server(
        eventlet.listen(('0.0.0.0', 3002)), 
        app,
        log_output=False
    )