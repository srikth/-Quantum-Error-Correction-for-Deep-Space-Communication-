import numpy as np

def encode_3qubit(state):
    return np.kron(np.kron(state, state), state)

def measure_syndrome(state):
    q1, q2, q3 = state[0:2], state[2:4], state[4:6]

    def parity(a, b):
        return int(np.argmax(np.abs(a)) != np.argmax(np.abs(b)))

    return (parity(q1, q2), parity(q2, q3))

def correct_error(state, syndrome):
    corrected = state.copy()

    if syndrome == (1, 0):
        idx = 0
    elif syndrome == (1, 1):
        idx = 1
    elif syndrome == (0, 1):
        idx = 2
    else:
        return corrected

    i = idx * 2
    corrected[i:i+2] = np.array([corrected[i+1], corrected[i]])
    return corrected

def decode_3qubit(state):
    q1, q2, q3 = state[0:2], state[2:4], state[4:6]

    votes = [
        np.argmax(np.abs(q1)),
        np.argmax(np.abs(q2)),
        np.argmax(np.abs(q3))
    ]

    majority = int(sum(votes) >= 2)

    return np.array([1, 0]) if majority == 0 else np.array([0, 1])
