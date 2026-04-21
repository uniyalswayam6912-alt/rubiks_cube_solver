import React from 'react';
import { Play, Square, RotateCcw } from 'lucide-react';

export default function Controls({ onPlay, onStop, onReset, isAnimating, disabled }) {
  return (
    <div className="flex gap-4 justify-center mt-4">
      <button
        onClick={onPlay}
        disabled={disabled || isAnimating}
        className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Play size={18} className={isAnimating ? "opacity-50" : ""} />
        Play
      </button>

      <button
        onClick={onStop}
        disabled={!isAnimating}
        className="flex items-center gap-2 px-5 py-2.5 bg-gray-600 hover:bg-gray-500 text-white rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Square size={18} />
        Stop
      </button>

      <button
        onClick={onReset}
        disabled={isAnimating}
        className="flex items-center gap-2 px-5 py-2.5 bg-slate-700 hover:bg-slate-600 text-white rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <RotateCcw size={18} />
        Reset
      </button>
    </div>
  );
}
