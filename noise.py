import numpy as np

def photon_loss_probability(distance, alpha=1e-9):
    return 1 - np.exp(-alpha * distance)

def amplitude_damping(state, gamma):
    K0 = np.array([[1, 0], [0, np.sqrt(1-gamma)]])
    K1 = np.array([[0, np.sqrt(gamma)], [0, 0]])

    noisy = K0 @ state + K1 @ state
    return noisy / np.linalg.norm(noisy)

def depolarizing_noise(state, p):
    if np.random.rand() > p:
        return state

    noise = np.random.choice(['X','Y','Z'])
    if noise == 'X':
        return np.array([state[1], state[0]])
    elif noise == 'Y':
        return np.array([1j*state[1], -1j*state[0]])
    elif noise == 'Z':
        return np.array([state[0], -state[1]])

def deep_space_noise(state, distance):
    p_loss = photon_loss_probability(distance)
    noisy = amplitude_damping(state, p_loss)
    noisy = depolarizing_noise(noisy, min(p_loss, 0.3))
    return noisy
