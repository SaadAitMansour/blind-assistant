import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default function Controls({ mode, connected }) {

  const switchMode = async (newMode) => {
    try {
      await axios.post(`${API_URL}/mode/${newMode}`);
    } catch (err) {
      console.error('Mode switch error:', err);
    }
  };

  const describeScene = async () => {
    try {
      await axios.post(`${API_URL}/scene`);
    } catch (err) {
      console.error('Scene error:', err);
    }
  };

  return (
    <div className="bg-gray-800 rounded-2xl p-5
                    border border-gray-700">

      <h2 className="text-white font-semibold
                     text-lg mb-4">
        🎮 Controls
      </h2>

      {/* Mode buttons */}
      <div className="grid grid-cols-2 gap-3 mb-4">

        {/* Detection mode */}
        <button
          onClick={() => switchMode('detection')}
          disabled={!connected}
          className={`
            py-3 px-4 rounded-xl font-semibold
            text-sm transition-all duration-200
            flex items-center justify-center gap-2
            ${mode === 'detection'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }
            ${!connected && 'opacity-50 cursor-not-allowed'}
          `}
        >
          🔍 Detection
        </button>

        {/* OCR mode */}
        <button
          onClick={() => switchMode('ocr')}
          disabled={!connected}
          className={`
            py-3 px-4 rounded-xl font-semibold
            text-sm transition-all duration-200
            flex items-center justify-center gap-2
            ${mode === 'ocr'
              ? 'bg-orange-600 text-white shadow-lg'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }
            ${!connected && 'opacity-50 cursor-not-allowed'}
          `}
        >
          📖 Text Reading
        </button>

      </div>

      {/* Scene button */}
      <button
        onClick={describeScene}
        disabled={!connected}
        className={`
          w-full py-3 rounded-xl font-semibold
          text-sm transition-all duration-200
          flex items-center justify-center gap-2
          bg-purple-600 text-white
          hover:bg-purple-700 active:scale-95
          ${!connected && 'opacity-50 cursor-not-allowed'}
        `}
      >
        📊 Describe Scene
      </button>

      {/* Info */}
      <div className="mt-4 bg-gray-900 rounded-xl p-3">
        <p className="text-gray-400 text-xs text-center">
          {mode === 'detection'
            ? '🔍 Detecting objects and distances'
            : '📖 Reading text from camera'
          }
        </p>
      </div>

    </div>
  );
}