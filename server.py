from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

from main import RubiksSolverV2
from cube.state import CubeState
from cube.moves import Move, apply_move

app = FastAPI()

# Enable CORS so the React frontend can fetch from it!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

solver = RubiksSolverV2()

class SolveRequest(BaseModel):
    moves: list[str]

@app.post("/solve")
def solve_cube(req: SolveRequest):
    # Enforce safe constraint limit in backend too!
    if len(req.moves) > 6:
        return {"error": "Maximum 6 moves allowed"}
        
    state = CubeState()
    for move_str in req.moves:
        try:
            state = apply_move(state, Move(move_str))
        except ValueError:
            return {"error": f"Invalid move: {move_str}"}

    start = time.time()
    try:
        # solve() returns a dict, handle safe execution
        result = solver.solve(state, verbose=False)
        return {
            "solution": [m.value for m in result['solution']],
            "move_count": len(result['solution']),
            "time": time.time() - start
        }
    except Exception as e:
        return {"error": "Solver timeout or failure: " + str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
