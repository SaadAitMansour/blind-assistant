export default function CameraFeed({ image, mode }) {
  return (
    <div className="bg-gray-900 rounded-2xl
                    overflow-hidden shadow-xl
                    border border-gray-700">

      {/* Camera header */}
      <div className="bg-gray-800 px-4 py-2
                      flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500"/>
          <div className="w-3 h-3 rounded-full bg-yellow-500"/>
          <div className="w-3 h-3 rounded-full bg-green-500"/>
        </div>
        <span className="text-gray-400 text-sm">
          📷 Live Camera
        </span>
        <span className={`text-xs px-2 py-1 rounded-full ${
          mode === 'detection'
            ? 'bg-blue-900 text-blue-300'
            : 'bg-orange-900 text-orange-300'
        }`}>
          {mode === 'detection'
            ? '🔍 Detection'
            : '📖 OCR'
          }
        </span>
      </div>

      {/* Camera feed */}
      {image ? (
        <img
          src={image}
          alt="Camera feed"
          className="w-full object-contain"
        />
      ) : (
        <div className="w-full h-80 flex items-center
                        justify-center bg-gray-800">
          <div className="text-center text-gray-500">
            <div className="text-5xl mb-3">📷</div>
            <p className="font-medium">
              Connecting to camera...
            </p>
            <div className="mt-3 w-8 h-8 border-4
                           border-blue-500
                           border-t-transparent
                           rounded-full animate-spin
                           mx-auto"/>
          </div>
        </div>
      )}
    </div>
  );
}