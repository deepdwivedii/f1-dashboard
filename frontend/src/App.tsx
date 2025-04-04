import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import LiveTiming from './components/LiveTiming';

const App = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [transport, setTransport] = useState("N/A");

  useEffect(() => {
    const socket = io(import.meta.env.VITE_API_URL || "http://localhost:3002", {
      transports: ["websocket"]
    });

    socket.on("connect", () => {
      setIsConnected(true);
      setTransport(socket.io.engine.transport.name);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="container">
      <p>Status: {isConnected ? "Connected" : "Disconnected"}</p>
      <p>Transport: {transport}</p>
      <LiveTiming />
    </div>
  );
};

export default App;