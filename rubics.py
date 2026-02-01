# Face order:
# 0-8: Upper(U)(white"W")
# 9-17: Right(R)(Red"R")
# 18-26: Front(F)(Green"G")
# 27-35: Down(D)(Yellow"Y")
# 36-44: Left(L)(Orange"O")
# 45-53: Back(B)(Blue"B")

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

if __name__ == "__main__":
    cube = SOLVED_STATE
    print_cube(cube) #print solved cube
    print("Solved:", is_solved(cube)) #checks if the cube is solved 

