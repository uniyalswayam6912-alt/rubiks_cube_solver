# Face order:
# 0-8: Upper(U)(white"W")
# 9-17: Right(R)(Red"R")
# 18-26: Front(F)(Green"G")
# 27-35: Down(D)(Yellow"Y")
# 36-44: Left(L)(Orange"O")
# 45-53: Back(B)(Blue"B")

from collections import deque
SOLVED_STATE= ("W"*9 + "R"*9 + "G"*9 + "Y"*9 + "O"*9 + "B"*9)

# SOLVED_STATE Sample: "WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"

#Checks if our cube is solved
def is_solved(state: str)-> bool: 
    return state == SOLVED_STATE

def print_face(state, start, name):
    face = state[start:start+9]
    print(f"{name}:")
    print(face[0], face[1], face[2])
    print(face[3], face[4], face[5])
    print(face[6], face[7], face[8])
    print()

#prints all faces of the cube
def print_cube(state: str):
    print_face(state, 0, "U")
    print_face(state, 9, "R")
    print_face(state, 18, "F")
    print_face(state, 27, "D")
    print_face(state, 36, "L")
    print_face(state, 45, "B")

def move_U(state:str)->str:
    s= list(state)
    new_s= s.copy()

    #now rotate U clockwise
    #dict key val pair 
    u_map = {
        0:6,1:3,2:0,
        3:7,4:4,5:1,
        6:8,7:5,8:2
    }

    for k,v in u_map.items():
        new_s[k] = s[v]

    #Top Row
    F = [18,19,20]
    R = [9, 10, 11]
    B = [45, 46, 47]
    L = [36, 37, 38]

    # Clockwise cycle (from top view):
    # F <- R <- B <- L <- F
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[F[0]], s[F[1]], s[F[2]]

    return "".join(new_s)  #makes list back into string

def move_U_prime(state:str)->str:
    s= list(state)
    new_s= s.copy()

    #now rotate U anti-clockwise
    u_map = {
        6:0,3:1,0:2,
        7:3,4:4,1:5,
        8:6,5:7,2:8
    }
    for k,v in u_map.items():
        new_s[k] = s[v]
    
    F = [18,19,20]
    R = [9, 10, 11]
    B = [45, 46, 47]
    L = [36, 37, 38]

    # Anti-Clockwise cycle (from top view):
    # F -> R -> B -> L -> F
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[B[0]], s[B[1]], s[B[2]]

    return "".join(new_s)

def move_R(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate R face clockwise (indices 9–17)
    r_map = {
        9:15, 10:12, 11:9,
        12:16, 13:13, 14:10,
        15:17, 16:14, 17:11
    }
    for k, v in r_map.items():
        new_s[k] = s[v]

    # Right column indices
    U = [2, 5, 8]
    F = [20, 23, 26]
    D = [29, 32, 35]
    B = [51, 48, 45]   # left column of B

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[U[0]], s[U[1]], s[U[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[D[0]], s[D[1]], s[D[2]]
    
    return "".join(new_s)

def move_R_prime(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate R face anti-clockwise (indices 9–17)
    r_map = {
        15:9, 12:10, 9:11,
        16:12, 13:13, 10:14,
        17:15, 14:16, 11:17
    }
    for k, v in r_map.items():
        new_s[k] = s[v]

    # Right column indices
    U = [2, 5, 8]
    F = [20, 23, 26]
    D = [29, 32, 35]
    B = [51, 48, 45]   # left column of B

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[D[0]], s[D[1]], s[D[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[U[0]], s[U[1]], s[U[2]]
    
    return "".join(new_s)

def move_F(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate F face clockwise (indices 18-26)
    f_map = {
        18:24, 19:21, 20:18,
        21:25, 22:22, 23:19,
        24:26, 25:23, 26:20
    }
    for k, v in f_map.items():
        new_s[k] = s[v]

    # Front column indices
    U = [6, 7, 8]
    R = [9, 12, 15]
    D = [29, 28, 27]
    L = [44, 41, 38]   # left column of F

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[U[0]], s[U[1]], s[U[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[D[0]], s[D[1]], s[D[2]]
    
    return "".join(new_s)

def move_F_prime(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate F face anti-clockwise (indices 18-26)
    f_map = {
        24:18, 21:19, 18:20,
        25:21, 22:22, 19:23,
        26:24, 23:25, 20:26
    }
    for k, v in f_map.items():
        new_s[k] = s[v]

    # Front column indices
    U = [6, 7, 8]
    R = [9, 12, 15]
    D = [29, 28, 27]
    L = [44, 41, 38]   # left column of F

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[D[0]], s[D[1]], s[D[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[U[0]], s[U[1]], s[U[2]]
    
    return "".join(new_s)

def move_L(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate L face clockwise (indices 18-26)
    f_map = {
        36:42, 37:39, 38:36,
        39:43, 40:40, 41:37,
        42:44, 43:41, 44:38
    }
    for k, v in f_map.items():
        new_s[k] = s[v]

    # Left column indices
    U = [0, 3, 6]
    F = [18, 21, 24]
    D = [27, 30, 33]
    B = [53, 50, 47]  

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[U[0]], s[U[1]], s[U[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[D[0]], s[D[1]], s[D[2]]
    
    return "".join(new_s)

def move_L_prime(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate L face anti-clockwise (indices 18-26)
    f_map = {
        42:36, 39:37, 36:38,
        43:39, 40:40, 37:41,
        44:42, 41:43, 38:44
    }
    for k, v in f_map.items():
        new_s[k] = s[v]

    # Left column indices
    U = [0, 3, 6]
    F = [18, 21, 24]
    D = [27, 30, 33]
    B = [53, 50, 47]  

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[D[0]], s[D[1]], s[D[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[U[0]], s[U[1]], s[U[2]]
    
    return "".join(new_s)

def move_D(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate D face clockwise
    d_map = {
        27:33, 28:30, 29:27,
        30:34, 31:31, 32:28,
        33:35, 34:32, 35:29
    }
    for k, v in d_map.items():
        new_s[k] = s[v]

    F = [24, 25, 26]
    R = [15, 16, 17]
    B = [51, 52, 53]   
    L = [42, 43, 44]

    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[L[0]], s[L[1]], s[L[2]]

    return "".join(new_s)

def move_D_prime(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    d_map = {
        33:27, 30:28, 27:29,
        34:30, 31:31, 28:32,
        35:33, 32:34, 29:35
    }
    for k, v in d_map.items():
        new_s[k] = s[v]

    F = [24, 25, 26]
    R = [15, 16, 17]
    B = [51, 52, 53]
    L = [42, 43, 44]

    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[F[0]], s[F[1]], s[F[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[B[0]], s[B[1]], s[B[2]]

    return "".join(new_s)

def move_B(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate B face clockwise
    b_map = {
        45:51, 46:48, 47:45,
        48:52, 49:49, 50:46,
        51:53, 52:50, 53:47
    }
    for k, v in b_map.items():
        new_s[k] = s[v]

    U = [2, 1, 0]
    R = [17, 14, 11]
    D = [33, 34, 35]
    L = [36, 39, 42]

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[D[0]], s[D[1]], s[D[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[U[0]], s[U[1]], s[U[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[L[0]], s[L[1]], s[L[2]]

    return "".join(new_s)

def move_B_prime(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    b_map = {
        51:45, 48:46, 45:47,
        52:48, 49:49, 46:50,
        53:51, 50:52, 47:53
    }
    for k, v in b_map.items():
        new_s[k] = s[v]

    U = [2, 1, 0]
    R = [17, 14, 11]
    D = [33, 34, 35]
    L = [36, 39, 42]

    new_s[U[0]], new_s[U[1]], new_s[U[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[U[0]], s[U[1]], s[U[2]]
    new_s[D[0]], new_s[D[1]], new_s[D[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[D[0]], s[D[1]], s[D[2]]

    return "".join(new_s)
 

MOVES = {
    "U": move_U,
    "U'": move_U_prime,
    "R": move_R,
    "R'": move_R_prime,
    "F": move_F,
    "F'":move_F_prime,
    "L":move_L,
    "L'":move_L_prime,
    "D": move_D,
    "D'":move_D_prime,
    "B":move_B,
    "B'":move_B_prime
}

def apply_move(state: str, move: str) -> str:
    return MOVES[move](state)

def is_bad_move(prev, curr):
    # if same move is done again
    if prev == curr:
        return True

    # inverse move
    if prev + "'" == curr or curr + "'" == prev:
        return True

    return False

def reconstruct_path(parent, move_used, end_state):
    path = []
    curr = end_state

    while parent[curr] is not None:
        path.append(move_used[curr])
        curr = parent[curr]

    path.reverse()
    return path

from collections import deque

def bfs(start_state: str):
    queue = deque([(start_state, None)])  # (state, last_move)
    visited = set([start_state])

    parent = {start_state: None}
    move_used = {start_state: None}

    while queue:
        curr, last_move = queue.popleft()

        if is_solved(curr):
            return reconstruct_path(parent, move_used, curr)

        for move in MOVES:
            if last_move and is_bad_move(last_move, move):
                continue

            next_state = apply_move(curr, move)

            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, move))

                parent[next_state] = curr
                move_used[next_state] = move

    return None

if __name__ == "__main__":
    for m in ["U","R","F","L","D","B"]:
        cube = SOLVED_STATE
        cube = apply_move(cube, m)
        cube = apply_move(cube, m+"'")
        assert cube == SOLVED_STATE

    # scrambling the cube
    scramble = ["U", "R", "F"]

    cube = SOLVED_STATE

    scramble = ["U","R","F","B"]
    for m in scramble:
        cube = apply_move(cube, m)

    solution = ["B'","F'","R'","U'"]
    for m in solution:
        cube = apply_move(cube, m)

    print("Solved?", cube == SOLVED_STATE)

