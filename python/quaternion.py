import numpy as np
import math


def rotatepoint(q, q_conju, point):
    u = np.append(0, point)
    temp1 = quat_mux(q, u)
    v = quat_mux(temp1, q_conju)

    rot = v[1:4, 0]

    return rot


def quat_mux(q0, q1):
    # Extract the values from Q0
    w0 = q0[0]
    x0 = q0[1]
    y0 = q0[2]
    z0 = q0[3]

    # Extract the values from Q1
    w1 = q1[0]
    x1 = q1[1]
    y1 = q1[2]
    z1 = q1[3]

    # Computer the product of the two quaternions, term by term
    qw = w0 * w1 - x0 * x1 - y0 * y1 - z0 * z1
    qx = w0 * x1 + x0 * w1 + y0 * z1 - z0 * y1
    qy = w0 * y1 - x0 * z1 + y0 * w1 + z0 * x1
    qz = w0 * z1 + x0 * y1 - y0 * x1 + z0 * w1

    # Create a 4 element array containing the final quaternion
    final_quaternion = np.array([qw, qx, qy, qz])

    # Return a 4 element array containing the final quaternion (q02,q12,q22,q32)
    return final_quaternion


def euler2quat(euler):
    # Uses ZYX conversion

    x = degToRad(euler[0])  # roll
    y = degToRad(euler[1])  # pitch
    z = degToRad(euler[2])  # yaw

    qw = np.cos(x / 2) * np.cos(y / 2) * np.cos(z / 2) + np.sin(x / 2) * np.sin(y / 2) * np.sin(z / 2)
    qx = np.sin(x / 2) * np.cos(y / 2) * np.cos(z / 2) - np.cos(x / 2) * np.sin(y / 2) * np.sin(z / 2)
    qy = np.cos(x / 2) * np.sin(y / 2) * np.cos(z / 2) + np.sin(x / 2) * np.cos(y / 2) * np.sin(z / 2)
    qz = np.cos(x / 2) * np.cos(y / 2) * np.sin(z / 2) - np.sin(x / 2) * np.sin(y / 2) * np.cos(z / 2)

    return np.array([[qw], [qx], [qy], [qz]])


def quatConjugate(quat):
    conjugate = np.array([quat[0], -quat[1], -quat[2], -quat[3]])
    return conjugate


def degToRad(deg):
    rad = deg * math.pi / 180
    return rad


def main():
    P = np.array([[1], [0], [0]])
    R = np.array([[0.707], [0], [0.707], [0]])

    R_prime = quatConjugate(R)

    rot = rotatepoint(R, R_prime, P)

    print(rot)


if __name__ == "__main__":
    main()
