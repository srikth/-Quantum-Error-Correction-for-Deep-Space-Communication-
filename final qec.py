import numpy as np

def logical_zero():
    basis = [
        "0000000","1010101","0110011","1100110",
        "0001111","1011010","0111100","1101001"
    ]

    state = np.zeros(128, dtype=complex)

    for b in basis:
        state[int(b, 2)] = 1

    return state / np.sqrt(8)
[00:49, 02/04/2026] Srikanth: import numpy as np

def photon_loss(distance, alpha=1e-9):
    return 1 - np.exp(-alpha * distance)

def apply_pauli(state, qubit, op_type):
    I = np.eye(2)
    X = np.array([[0,1],[1,0]])
    Z = np.array([[1,0],[0,-1]])
    Y = 1j * X @ Z

    ops = [I]*7

    if op_type == 'X': ops[qubit] = X
    elif op_type == 'Y': ops[qubit] = Y
    elif op_type == 'Z': ops[qubit] = Z

    op = ops[0]
    for o in ops[1:]:
        op = np.kron(op, o)

    return op @ state

def deep_space_noise(state, distance):
    p = photon_loss(distance)

    for q in range(7):
        if np.random.rand() < p:
            error = np.random.choice(['X','Y','Z'])
            state = apply_pauli(state, q, error)

    return state / np.linalg.norm(state)
