import { useState, useEffect, useRef } from 'react';

const WS_URL = 'ws://localhost:8000/ws';

export default function useWebSocket() {
  const [image,      setImage]      = useState(null);
  const [detections, setDetections] = useState([]);
  const [text,       setText]       = useState(null);
  const [speaking,   setSpeaking]   = useState(false);
  const [connected,  setConnected]  = useState(false);
  const [mode,       setMode]       = useState('detection');
  const ws = useRef(null);

  useEffect(() => {
    connect();
    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const connect = () => {
    console.log('🔄 Connecting to WebSocket...');
    ws.current = new WebSocket(WS_URL);

    // Connected
    ws.current.onopen = () => {
      console.log('✅ WebSocket connected!');
      setConnected(true);
    };

    // Message received
    ws.current.onmessage = (event) => {
      const payload = JSON.parse(event.data);

      if (payload.image) {
        setImage(payload.image);
      }

      if (payload.data) {
        setDetections(payload.data.detections || []);
        setText(payload.data.text       || null);
        setSpeaking(payload.data.speaking || false);
        setMode(payload.data.mode       || 'detection');
      }
    };

    // Disconnected
    ws.current.onclose = () => {
      console.log('❌ WebSocket disconnected!');
      setConnected(false);
      // Reconnect after 2 seconds
      setTimeout(connect, 2000);
    };

    // Error
    ws.current.onerror = (err) => {
      console.error('❌ WebSocket error:', err);
      setConnected(false);
    };
  };

  return {
    image,
    detections,
    text,
    speaking,
    connected,
    mode,
  };
}