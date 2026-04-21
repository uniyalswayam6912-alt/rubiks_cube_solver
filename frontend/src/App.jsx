import React, { useState, useEffect, useRef } from 'react';
import Cube3D from './components/Cube3D';
import MoveControls from './components/MoveControls';
import ScramblePanel from './components/ScramblePanel';
import SolutionPanel from './components/SolutionPanel';
import Controls from './components/Controls';
import { initialCubeState, applyMoveToState } from './cubeLogic';
import { fetchSolution } from './api';

const MOVES_LIST = ["U", "U'", "U2", "D", "D'", "D2", "L", "L'", "L2", "R", "R'", "R2", "F", "F'", "F2", "B", "B'", "B2"];

function App() {
  const [cubeState, setCubeState] = useState(initialCubeState());
  const [scrambleMoves, setScrambleMoves] = useState([]);
  const [solutionData, setSolutionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);

  const animationQueue = useRef([]);
  const animFrameId = useRef(null);

  const handleMoveClick = (move) => {
    if (scrambleMoves.length >= 6) {
      alert("Maximum 6 moves allowed.");
      return;
    }
    setScrambleMoves(prev => [...prev, move]);
    setCubeState(prev => applyMoveToState(prev, move));
    setSolutionData(null);
    setError(null);
  };

  const handleClear = () => {
    setScrambleMoves([]);
    setCubeState(initialCubeState());
    setSolutionData(null);
    setError(null);
    stopAnimation();
  };

  const handleRandom = () => {
    const length = Math.floor(Math.random() * 2) + 5;
    const newScramble = [];
    let state = initialCubeState();

    for (let i = 0; i < length; i++) {
      const randomMove = MOVES_LIST[Math.floor(Math.random() * MOVES_LIST.length)];
      newScramble.push(randomMove);
      state = applyMoveToState(state, randomMove);
    }

    setScrambleMoves(newScramble);
    setCubeState(state);
    setSolutionData(null);
    setError(null);
    stopAnimation();
  };

  const handleSolve = async () => {
    if (scrambleMoves.length === 0) return;
    
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSolution(scrambleMoves);
      setSolutionData(data);
    } catch (err) {
      setError("Solver timeout or error. Try ≤6 moves.");
    } finally {
      setLoading(false);
    }
  };

  const playAnimation = () => {
    if (!solutionData || solutionData.solution.length === 0) return;
    
    setIsAnimating(true);
    animationQueue.current = [...solutionData.solution];
    
    const applyNextMove = () => {
      if (animationQueue.current.length === 0) {
        setIsAnimating(false);
        return;
      }
      
      const nextMove = animationQueue.current.shift();
      setCubeState(prev => applyMoveToState(prev, nextMove));
      
      // Delay before next move application
      animFrameId.current = setTimeout(applyNextMove, 500); 
    };

    applyNextMove();
  };

  const stopAnimation = () => {
    if (animFrameId.current) {
      clearTimeout(animFrameId.current);
    }
    animationQueue.current = [];
    setIsAnimating(false);
  };

  return (
    <div className="min-h-screen p-8 max-w-5xl mx-auto flex flex-col gap-6">
      
      <header className="text-center mb-6">
        <h1 className="text-3xl font-semibold text-white">
          Rubik's Cube Solver
        </h1>
        <p className="text-gray-400 mt-2">Limited to 6 moves.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Cube & Controls */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          <Cube3D cubeState={cubeState} />
          <Controls 
            onPlay={playAnimation}
            onStop={stopAnimation}
            onReset={handleClear}
            isAnimating={isAnimating}
            disabled={!solutionData || solutionData.solution.length === 0}
          />
        </div>

        {/* Right Column: Panels */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <ScramblePanel 
            scramble={scrambleMoves}
            onClear={handleClear}
            onRandom={handleRandom}
            disabled={loading || isAnimating}
          />
          
          <MoveControls 
            onMoveClick={handleMoveClick}
            disabled={loading || isAnimating || scrambleMoves.length >= 6}
          />

          <button
            onClick={handleSolve}
            disabled={scrambleMoves.length === 0 || loading || isAnimating}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Solving...' : 'Solve'}
          </button>

          <SolutionPanel 
            solutionData={solutionData} 
            loading={loading} 
            error={error} 
            scrambleLength={scrambleMoves.length}
          />
        </div>

      </div>
    </div>
  );
}

export default App;
