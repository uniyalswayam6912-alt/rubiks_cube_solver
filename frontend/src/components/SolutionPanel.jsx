import React from 'react';

export default function SolutionPanel({ solutionData, loading, error, scrambleLength }) {
  if (loading) {
    return (
      <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center animate-pulse">
        <p className="text-gray-400 font-medium">Solving...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/30 p-4 rounded-xl border border-red-700/50 text-center">
        <p className="text-red-400 font-medium">{error}</p>
      </div>
    );
  }

  if (!solutionData) {
    return null;
  }

  return (
    <div className="bg-slate-800 p-4 rounded-xl border border-slate-700">
      <h3 className="text-sm font-medium text-gray-400 mb-2">Solution</h3>
      <div className="space-y-2">
        <div className="flex gap-2 items-start">
          <span className="text-slate-500 font-semibold w-16">Moves:</span>
          <div className="flex-1 flex flex-wrap gap-1">
            {solutionData.solution.map((move, i) => (
              <span key={i} className="bg-blue-900/50 text-blue-300 px-2 py-0.5 rounded font-mono font-bold text-sm">
                {move}
              </span>
            ))}
          </div>
        </div>
        <div className="flex gap-2">
          <span className="text-slate-500 font-semibold w-16">Count:</span>
          <span className="text-white font-mono">{solutionData.move_count}</span>
        </div>
        <div className="flex gap-2">
          <span className="text-slate-500 font-semibold w-16">Time:</span>
          <span className="text-white font-mono">{Number(solutionData.total_time || solutionData.time || 0).toFixed(2)}s</span>
        </div>
      </div>
    </div>
  );
}
