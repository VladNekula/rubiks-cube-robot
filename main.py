from camera import scan_face
from solver import solve_cube

faces = ["U", "R", "F", "D", "L", "B"]

cube = {}

for face in faces:

    print(f"Покажите сторону {face} и нажмите Space в окне камеры")

    colors = scan_face()

    cube[face] = colors
    print(face, "считано")

print("Решение:")

solution = solve_cube(cube)

print(solution)
