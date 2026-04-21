import useWebSocket   from './hooks/useWebSocket';
import Header         from './components/Header';
import CameraFeed     from './components/CameraFeed';
import Controls       from './components/Controls';
import DetectionList  from './components/DetectionList';
import StatusBar      from './components/StatusBar';

export default function App() {
  const {
    image,
    detections,
    text,
    speaking,
    connected,
    mode,
  } = useWebSocket();

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* Header */}
      <Header
        connected={connected}
        speaking={speaking}
      />

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-6">

        {/* Status Bar */}
        <div className="mb-6">
          <StatusBar
            connected={connected}
            speaking={speaking}
            mode={mode}
            detections={detections}
          />
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1
                       lg:grid-cols-3 gap-6">

          {/* Camera - takes 2 columns */}
          <div className="lg:col-span-2">
            <CameraFeed
              image={image}
              mode={mode}
            />
          </div>

          {/* Right panel */}
          <div className="space-y-4">
            <Controls
              mode={mode}
              connected={connected}
            />
            <DetectionList
              detections={detections}
              text={text}
              mode={mode}
            />
          </div>

        </div>
      </main>

    </div>
  );
}