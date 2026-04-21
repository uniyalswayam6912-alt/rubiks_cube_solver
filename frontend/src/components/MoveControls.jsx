import React from 'react';

const MOVES = [
  "U", "U'", "U2",
  "D", "D'", "D2",
  "L", "L'", "L2",
  "R", "R'", "R2",
  "F", "F'", "F2",
  "B", "B'", "B2"
];

export default function MoveControls({ onMoveClick, disabled }) {
  return (
    <div className="bg-slate-800 p-4 rounded-xl border border-slate-700">
      <h3 className="text-sm font-medium text-gray-400 mb-3">Input Moves</h3>
      <div className="grid grid-cols-3 gap-2">
        {MOVES.map((move) => (
          <button
            key={move}
            onClick={() => onMoveClick(move)}
            disabled={disabled}
            className={`px-3 py-2 rounded font-semibold transition-colors
              ${disabled 
                ? 'bg-slate-700/50 text-slate-500 cursor-not-allowed' 
                : 'bg-slate-700 hover:bg-blue-600 hover:text-white'}`}
          >
            {move}
          </button>
        ))}
      </div>
      {disabled && (
        <p className="text-red-400 text-xs text-center mt-3 font-medium">
          Maximum 6 moves allowed
        </p>
      )}
    </div>
  );
}
