import React from 'react';

export default function ScramblePanel({ scramble, onClear, onRandom, disabled }) {
  return (
    <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 flex justify-between items-center">
      <div className="flex-1">
        <h3 className="text-sm font-medium text-gray-400 mb-1">Current Scramble</h3>
        <div className="flex flex-wrap gap-2 min-h-[32px]">
          {scramble.length === 0 ? (
            <span className="text-slate-500 italic">No moves added</span>
          ) : (
            scramble.map((move, index) => (
              <span key={index} className="bg-slate-700 px-2 py-1 rounded text-white font-mono font-bold">
                {move}
              </span>
            ))
          )}
        </div>
      </div>
      
      <div className="flex gap-2 ml-4">
        <button 
          onClick={onClear}
          disabled={disabled || scramble.length === 0}
          className="px-4 py-2 bg-slate-700 hover:bg-gray-600 text-white rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Clear
        </button>
        <button 
          onClick={onRandom}
          disabled={disabled}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Random
        </button>
      </div>
    </div>
  );
}
