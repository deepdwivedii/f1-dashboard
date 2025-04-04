import fastf1
from flask import Flask
from flask_cors import CORS
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)
CORS(app)

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
    sio.start_background_task(emit_live_data)
    app = socketio.WSGIApp(sio, app)
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 3002)), app)