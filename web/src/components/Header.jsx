export default function Header({ connected, speaking }) {
  return (
    <header className="bg-gray-900 text-white py-4 px-6
                       shadow-lg border-b border-gray-700">
      <div className="max-w-6xl mx-auto
                      flex items-center justify-between">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <span className="text-3xl">👁️</span>
          <div>
            <h1 className="text-xl font-bold">
              Blind Assistant
            </h1>
            <p className="text-gray-400 text-xs">
              AI Powered Vision Assistant
            </p>
          </div>
        </div>

        {/* Status indicators */}
        <div className="flex items-center gap-4">

          {/* Speaking indicator */}
          {speaking && (
            <div className="flex items-center gap-2
                           bg-green-900 px-3 py-1
                           rounded-full animate-pulse">
              <span className="text-sm">🔊</span>
              <span className="text-green-400
                               text-sm font-medium">
                Speaking...
              </span>
            </div>
          )}

          {/* Connection indicator */}
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${
              connected
                ? 'bg-green-500 animate-pulse'
                : 'bg-red-500'
            }`}/>
            <span className="text-sm text-gray-400">
              {connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

        </div>
      </div>
    </header>
  );
}