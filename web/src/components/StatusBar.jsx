export default function StatusBar({
  connected, speaking, mode, detections
}) {

  const dangerCount = detections.filter(
    d => d.danger === 'DANGER'
  ).length;

  return (
    <div className={`
      rounded-2xl p-4 border
      ${dangerCount > 0
        ? 'bg-red-900/30 border-red-500'
        : 'bg-gray-800 border-gray-700'
      }
    `}>
      <div className="flex items-center
                     justify-between flex-wrap gap-3">

        {/* Connection */}
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${
            connected ? 'bg-green-500' : 'bg-red-500'
          }`}/>
          <span className="text-gray-400 text-sm">
            {connected ? 'Live' : 'Offline'}
          </span>
        </div>

        {/* Mode */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm">
            Mode:
          </span>
          <span className={`text-sm font-semibold ${
            mode === 'detection'
              ? 'text-blue-400'
              : 'text-orange-400'
          }`}>
            {mode === 'detection'
              ? '🔍 Detection'
              : '📖 OCR'
            }
          </span>
        </div>

        {/* Objects */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm">
            Objects:
          </span>
          <span className="text-white font-semibold text-sm">
            {detections.length}
          </span>
        </div>

        {/* Speaking */}
        <div className="flex items-center gap-2">
          {speaking ? (
            <span className="text-green-400
                            text-sm animate-pulse">
              🔊 Speaking...
            </span>
          ) : (
            <span className="text-gray-500 text-sm">
              🔇 Ready
            </span>
          )}
        </div>

        {/* Danger alert */}
        {dangerCount > 0 && (
          <div className="flex items-center gap-2
                         bg-red-500 px-3 py-1
                         rounded-full animate-pulse">
            <span className="text-white text-sm font-bold">
              ⚠️ {dangerCount} DANGER!
            </span>
          </div>
        )}

      </div>
    </div>
  );
}