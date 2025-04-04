from flask import Flask, jsonify
from flask_cors import CORS
import socketio
import eventlet
import fastf1
import numpy as np

sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
app = Flask(__name__)
CORS(app)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Track normalization parameters
TRACK_BOUNDS = {
    'minX': -2500,
    'maxX': 2500,
    'minY': -1500,
    'maxY': 1500
}

TEAM_COLORS = {
    'Mercedes': '#00D2BE',
    'Red Bull': '#0600EF',
    'Ferrari': '#DC0000',
    'McLaren': '#FF8700',
    'Alpine': '#0090FF',
    'Aston Martin': '#006F62',
    'AlphaTauri': '#2B4562',
    'Alfa Romeo': '#900000',
    'Haas': '#FFFFFF',
    'Williams': '#005AFF'
}

@app.route('/')
def health_check():
    return jsonify({"status": "live", "track": "Barcelona"})

def normalize_position(val, min_val, max_val):
    return ((val - min_val) / (max_val - min_val)) * 100

def emit_f1_data():
    session = fastf1.get_session(2023, 'Spain', 'Q')
    session.load()
    
    # Get track reference data
    lap = session.laps.pick_first()
    tel = lap.get_telemetry()
    
    global TRACK_BOUNDS
    TRACK_BOUNDS = {
        'minX': np.min(tel['X']),
        'maxX': np.max(tel['X']),
        'minY': np.min(tel['Y']),
        'maxY': np.max(tel['Y'])
    }

    while True:
        try:
            live_data = session.get_live_data()
            positions = []
            
            for driver in live_data.drivers:
                car_data = live_data.get_driver(driver).get_car_data()
                
                positions.append({
                    'number': driver,
                    'driverCode': live_data.get_driver(driver).get_abbreviation(),
                    'x': car_data['X'].iloc[-1],
                    'y': car_data['Y'].iloc[-1],
                    'speed': car_data['Speed'].iloc[-1],
                    'team': live_data.get_driver(driver).get_team(),
                    'inPit': live_data.get_driver(driver).get_in_pit()
                })
            
            # Normalize and format data
            normalized = [{
                'number': p['number'],
                'driverCode': p['driverCode'],
                'x': p['x'],
                'y': p['y'],
                'speed': p['speed'],
                'teamColor': TEAM_COLORS.get(p['team'], '#FFFFFF'),
                'inPit': p['inPit']
            } for p in positions]

            sio.emit('f1_update', normalized)
            eventlet.sleep(0.2)
            
        except Exception as e:
            print(f"Data error: {str(e)}")
            eventlet.sleep(1)

if __name__ == '__main__':
    eventlet.spawn(emit_f1_data)
    eventlet.wsgi.server(
        eventlet.listen(('0.0.0.0', 3002)),
        app,
        log_output=False
    )