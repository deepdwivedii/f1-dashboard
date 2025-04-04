// frontend/src/components/TrackMap.tsx
import { useEffect, useState } from 'react';

interface CarPosition {
  number: string;
  driverCode: string;
  x: number;
  y: number;
  teamColor: string;
  inPit: boolean;
  speed: number;
}

// Track dimensions (Circuit de Barcelona-Catalunya example)
const TRACK_BOUNDS = {
  minX: -2500,
  maxX: 2500,
  minY: -1500,
  maxY: 1500
};

const TEAM_COLORS: { [key: string]: string } = {
  'Mercedes': '#00D2BE',
  'Red Bull Racing': '#0600EF',
  'Ferrari': '#DC0000',
  'McLaren': '#FF8700',
  'Alpine': '#0090FF',
  'Aston Martin': '#006F62',
  'AlphaTauri': '#2B4562',
  'Alfa Romeo': '#900000',
  'Haas F1 Team': '#FFFFFF',
  'Williams': '#005AFF'
};

const TrackMap = ({ cars }: { cars: CarPosition[] }) => {
  const [viewport, setViewport] = useState({ width: 300, height: 150 });

  // Normalize telemetry data to SVG coordinates
  const normalizeX = (x: number) => 
    ((x - TRACK_BOUNDS.minX) / (TRACK_BOUNDS.maxX - TRACK_BOUNDS.minX)) * 100;

  const normalizeY = (y: number) => 
    100 - ((y - TRACK_BOUNDS.minY) / (TRACK_BOUNDS.maxY - TRACK_BOUNDS.minY)) * 100;

  // Responsive sizing
  useEffect(() => {
    const handleResize = () => {
      setViewport({
        width: Math.min(window.innerWidth - 40, 600),
        height: Math.min(window.innerWidth * 0.4, 300)
      });
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="track-map bg-gray-900 p-4 rounded-xl shadow-xl">
      <svg 
        viewBox="0 0 100 100" 
        width={viewport.width} 
        height={viewport.height}
      >
        {/* Track Outline */}
        <path
          d="M 10,50 Q 25,25 40,50 T 70,50 Q 85,75 90,50 T 110,50"
          fill="none"
          stroke="#444"
          strokeWidth="0.8"
          strokeLinecap="round"
        />
        
        {/* Cars */}
        {cars.map((car) => (
          <g
            key={car.number}
            transform={`translate(${normalizeX(car.x)},${normalizeY(car.y)})`}
            className="transition-all duration-500 ease-linear"
          >
            <rect
              x="-3" y="-2"
              width="6" height="4"
              fill={car.teamColor}
              rx="1"
              className={`${car.inPit ? 'opacity-50' : ''} shadow-lg`}
            />
            <text
              x="0" y="-6"
              textAnchor="middle"
              fontSize="3"
              fill="white"
              className="font-bold"
            >
              {car.number}
            </text>
            <text
              x="0" y="8"
              textAnchor="middle"
              fontSize="2.5"
              fill="#ccc"
            >
              {Math.round(car.speed)}kph
            </text>
            {car.inPit && (
              <circle cx="5" cy="0" r="1.5" fill="#FFD700" />
            )}
          </g>
        ))}
      </svg>
    </div>
  );
};

export default TrackMap;