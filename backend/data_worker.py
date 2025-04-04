from flask import Flask, jsonify
from flask_cors import CORS
import socketio
import fastf1
import eventlet

# Initialize Flask and Socket.IO
app = Flask(__name__)
CORS(app)
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
wsgi_app = socketio.WSGIApp(sio, app)

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({"status": "ok", "message": "F1 Data Server Running"})

# WebSocket events
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

def emit_f1_data():
    session = fastf1.get_session(2023, 'Spain', 'Q')
    session.load()
    
    while True:
        lap_data = session.laps.to_dict('records')
        sio.emit('f1_update', lap_data[:20])
        eventlet.sleep(1)

if __name__ == '__main__':
    # Start data emitter in background
    eventlet.spawn(emit_f1_data)
    
    # Start server
    eventlet.wsgi.server(
        eventlet.listen(('0.0.0.0', 3002)),
        wsgi_app,
        log_output=False
    )