export default function DetectionList({
  detections, text, mode
}) {

  const dangerColors = {
    DANGER:  'border-red-500    bg-red-900/30    text-red-400',
    WARNING: 'border-orange-500 bg-orange-900/30 text-orange-400',
    NEAR:    'border-yellow-500 bg-yellow-900/30 text-yellow-400',
    FAR:     'border-green-500  bg-green-900/30  text-green-400',
  };

  const dangerIcons = {
    DANGER:  '🔴',
    WARNING: '🟠',
    NEAR:    '🟡',
    FAR:     '🟢',
  };

  return (
    <div className="bg-gray-800 rounded-2xl p-5
                    border border-gray-700">

      <h2 className="text-white font-semibold
                     text-lg mb-4">
        {mode === 'detection'
          ? '🔍 Detections'
          : '📖 Text Found'
        }
      </h2>

      {/* Detection Mode */}
      {mode === 'detection' && (
        <>
          {detections.length > 0 ? (
            <div className="space-y-2 max-h-80
                           overflow-y-auto">
              {detections.map((det, idx) => (
                <div
                  key={idx}
                  className={`
                    border rounded-xl p-3
                    ${dangerColors[det.danger]
                      || dangerColors.FAR}
                  `}
                >
                  <div className="flex items-center
                                 justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <span>
                        {dangerIcons[det.danger] || '🟢'}
                      </span>
                      <span className="text-white
                                      font-semibold
                                      capitalize">
                        {det.label}
                      </span>
                    </div>
                    <span className="text-xs px-2 py-0.5
                                    rounded-full font-medium
                                    bg-gray-700 text-gray-300">
                      {det.danger}
                    </span>
                  </div>
                  <div className="flex items-center
                                 gap-3 text-sm
                                 text-gray-300">
                    <span>📍 {det.direction}</span>
                    <span>📏 {det.distance}cm</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-10
                           text-gray-500">
              <div className="text-4xl mb-2">👁️</div>
              <p>No objects detected</p>
            </div>
          )}

          {/* Summary */}
          {detections.length > 0 && (
            <div className="mt-3 pt-3 border-t
                           border-gray-700">
              <p className="text-gray-400 text-sm">
                Total:
                <span className="text-white
                                font-bold ml-1">
                  {detections.length} objects
                </span>
              </p>
              {detections.filter(
                d => d.danger === 'DANGER'
              ).length > 0 && (
                <p className="text-red-400 text-sm mt-1">
                  ⚠️ {detections.filter(
                    d => d.danger === 'DANGER'
                  ).length} very close!
                </p>
              )}
            </div>
          )}
        </>
      )}

      {/* OCR Mode */}
      {mode === 'ocr' && (
        <>
          {text ? (
            <div className="bg-gray-900 rounded-xl p-4
                           border border-gray-600">
              <p className="text-green-400
                           font-medium mb-2 text-sm">
                ✅ Text detected:
              </p>
              <p className="text-white text-lg
                           font-semibold">
                {text}
              </p>
            </div>
          ) : (
            <div className="text-center py-10
                           text-gray-500">
              <div className="text-4xl mb-2">📖</div>
              <p>Point camera at text</p>
            </div>
          )}
        </>
      )}

    </div>
  );
}