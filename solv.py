import kociemba

color_to_face = {
    "W": "U",
    "Y": "D",
    "R": "R",
    "O": "L",
    "G": "F",
    "B": "B"
}

def cube_to_string(cube):
    order = ["U", "R", "F", "D", "L", "B"]
    result = ""

    for face in order:
        for row in cube[face]:
            for color in row:
                result += color_to_face[color]

    return result

def solve_cube(cube):
    try:
        cube_string = cube_to_string(cube)
        solution = kociemba.solve(cube_string)
        return solution

    except Exception as e:
        return f"Ошибка: {str(e)}"
