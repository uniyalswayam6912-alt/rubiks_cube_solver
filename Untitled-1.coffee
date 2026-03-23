def move_U(state: str) -> str:
    s = list(state)
    new_s = s.copy()

    # Rotate U face clockwise (0-8)
    u_map = {
        0: 6, 1: 3, 2: 0,
        3: 7, 4: 4, 5: 1,
        6: 8, 7: 5, 8: 2
    }

    for k, v in u_map.items():
        new_s[k] = s[v]

    # Top rows
    F = [18, 19, 20]
    R = [9, 10, 11]
    B = [45, 46, 47]
    L = [36, 37, 38]

    # Clockwise cycle (from top view):
    # F <- R <- B <- L <- F
    new_s[F[0]], new_s[F[1]], new_s[F[2]] = s[R[0]], s[R[1]], s[R[2]]
    new_s[R[0]], new_s[R[1]], new_s[R[2]] = s[B[0]], s[B[1]], s[B[2]]
    new_s[B[0]], new_s[B[1]], new_s[B[2]] = s[L[0]], s[L[1]], s[L[2]]
    new_s[L[0]], new_s[L[1]], new_s[L[2]] = s[F[0]], s[F[1]], s[F[2]]

    return "".join(new_s)  #makes list back to string
