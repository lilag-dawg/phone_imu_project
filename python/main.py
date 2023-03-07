import socket
import pygame
import numpy as np
import quaternion


def manageData(raw_data):
    data = raw_data.decode()
    d = data.split(",")

    euler_orientation = [None, None, None]

    if len(d) >= 17:
        euler_orientation[0] = float(d[14])
        euler_orientation[1] = float(d[15])
        euler_orientation[2] = float(d[16])

    return euler_orientation


def manageDrawing(screen, cube_points, project_matrix, quat):
    screen.fill((0, 0, 0))

    scale = 50
    offset = 300

    quat_conju = quaternion.quatConjugate(quat)

    for point in cube_points:
        rot = quaternion.rotatepoint(quat, quat_conju, point)

        p_2d = np.matmul(project_matrix, rot)

        x = p_2d.item(0) * scale + offset
        y = p_2d.item(1) * scale + offset

        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)


def main():
    # UCP initialization
    host = ''
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))

    # Pygame initialization
    pygame.init()

    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)

    # Points to draw
    cube_points = [None] * 8
    cube_points[0] = np.array([[1], [-2], [-3]])
    cube_points[1] = np.array([[1], [2], [-3]])
    cube_points[2] = np.array([[1], [-2], [3]])
    cube_points[3] = np.array([[1], [2], [3]])
    cube_points[4] = np.array([[-1], [-2], [-3]])
    cube_points[5] = np.array([[-1], [2], [-3]])
    cube_points[6] = np.array([[-1], [-2], [3]])
    cube_points[7] = np.array([[-1], [2], [3]])

    # Projection matrix
    project_matrix = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])

    while True:
        try:
            data, address = s.recvfrom(8192)

        except (KeyboardInterrupt, SystemExit):
            print('Programmed Closed')
            pygame.quit()
            exit()

        else:
            euler = manageData(data)

            if euler[0] is not None:
                quat = quaternion.euler2quat(euler)
                manageDrawing(screen, cube_points, project_matrix, quat)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()


if __name__ == "__main__":
    main()
