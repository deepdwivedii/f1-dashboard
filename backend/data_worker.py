import fastf1
from flask import Flask
from flask_cors import CORS
import socketio


app = Flask(__name__)
CORS(app)
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')

app = socketio.WSGIApp(sio, app)

@app.route('/')
def home():
    return "F1 Data Server"

def emit_live_data():
    session = fastf1.get_session(2023, 'Spain', 'Q')  # Test with cached session
    session.load()
    
    while True:
        lap_data = session.laps.to_dict('records')
        sio.emit('f1Live', lap_data[:20])  # Send top 20 cars
        sio.sleep(1)  # Update interval

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(
        eventlet.listen(('0.0.0.0', 3002)),  # Explicit port binding
        app,
        log_output=False
    )