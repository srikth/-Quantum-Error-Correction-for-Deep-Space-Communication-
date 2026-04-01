import numpy as np
from src.qec import encode_3qubit, measure_syndrome, correct_error, decode_3qubit
from src.noise import deep_space_noise

def random_qubit():
    theta = np.random.rand() * np.pi
    phi = np.random.rand() * 2 * np.pi
    return np.array([
        np.cos(theta/2),
        np.exp(1j*phi) * np.sin(theta/2)
    ])

def fidelity(a, b):
    return np.abs(np.vdot(a, b))**2

def run_simulation():
    distances = np.linspace(1e3, 2.25e8, 30)

    f_before, f_after = [], []

    for d in distances:
        q = random_qubit()
        encoded = encode_3qubit(q)

        noisy = encoded.copy()
        for i in range(3):
            noisy[i*2:(i+1)*2] = deep_space_noise(noisy[i*2:(i+1)*2], d)

        f_before.append(fidelity(q, noisy[:2]))

        syndrome = measure_syndrome(noisy)
        corrected = correct_error(noisy, syndrome)
        decoded = decode_3qubit(corrected)

        f_after.append(fidelity(q, decoded))

    return distances, f_before, f_after
