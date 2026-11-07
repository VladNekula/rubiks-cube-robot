import kociemba

color_to_face = {

    "W": "U",
    "R": "R",
    "G": "F",
    "Y": "D",
    "O": "L",
    "B": "B"
}

def cube_to_string(cube):

    order = ["U", "R", "F", "D", "L", "B"]

    cube_string = ""

    for face in order:

        for row in cube[face]:

            for color in row:

                cube_string += color_to_face[color]

    return cube_string

def solve_cube(cube):

    cube_string = cube_to_string(cube)

    solution = kociemba.solve(cube_string)

    return solution
