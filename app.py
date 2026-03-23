from flask import Flask, render_template, request, jsonify
from rubiks import *   # IMPORTANT: your backend file name

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()

    if not data or "scramble" not in data:
        return jsonify({
            "solution": None,
            "status": "Invalid input"
        })

    scramble_input = data["scramble"].strip()
    moves_list = scramble_input.split()

    #  TO Validate moves
    valid_moves = set(MOVES.keys())
    for m in moves_list:
        if m not in valid_moves:
            return jsonify({
                "solution": None,
                "status": f"Invalid move: {m}"
            })

    # scrambling
    cube = SOLVED_STATE
    for m in moves_list:
        cube = apply_move(cube, m)

    # Currently solving using BFS
    solution = bfs(cube)

    if solution is None:
        return jsonify({
            "solution": None,
            "status": "Too deep / not found"
        })

    return jsonify({
        "solution": solution,
        "status": "Solved"
    })


if __name__ == "__main__":
    app.run(debug=True)