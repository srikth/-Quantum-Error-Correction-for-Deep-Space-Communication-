import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
 1. STEANE CODE


def logical_zero():
    basis = [
        "0000000","1010101","0110011","1100110",
        "0001111","1011010","0111100","1101001"
    ]
    state = np.zeros(128, dtype=complex)
    for b in basis:
        state[int(b, 2)] = 1
    return state / np.sqrt(8)


 2. NOISE MODEL


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

    state = state / np.linalg.norm(state)
    return state


 3. FEATURE EXTRACTION


def extract_features(state):
    return np.concatenate([np.real(state), np.imag(state)])

 4. AI MODEL


class QuantumDecoder(nn.Module):
    def _init_(self):
        super()._init_()
        self.net = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 28)
        )

    def forward(self, x):
        return self.net(x)

 5. DATA GENERATION


def generate_dataset(N=5000):
    X, y = [], []

    for _ in range(N):
        state = logical_zero()
        distance = np.random.choice([1e3, 384400, 2.25e8])

        noisy = state.copy()
        label = 0

        # Inject one random error for training
        if np.random.rand() < 0.7:
            qubit = np.random.randint(0,7)
            error = np.random.choice(['X','Y','Z'])
            noisy = apply_pauli(noisy, qubit, error)

            error_map = {'I':0,'X':1,'Y':2,'Z':3}
            label = qubit * 4 + error_map[error]

        X.append(extract_features(noisy))
        y.append(label)

    return np.array(X), np.array(y)

 6. TRAINING


def train_model(X, y):
    model = QuantumDecoder()

    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y, dtype=torch.long)

    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(50):
        optimizer.zero_grad()
        output = model(X_t)
        loss = loss_fn(output, y_t)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    return model

 7. CORRECTION LOGIC


def decode_prediction(pred):
    pred_class = torch.argmax(pred).item()
    qubit = pred_class // 4
    error_type_idx = pred_class % 4
    error_map = {0:'I',1:'X',2:'Y',3:'Z'}
    return qubit, error_map[error_type_idx]


def apply_correction(state, qubit, error_type):
    if error_type == 'I':
        return state
    return apply_pauli(state, qubit, error_type)

 8. SIMULATION


def fidelity(a, b):
    return abs(np.vdot(a, b))**2


def run_simulation(model):
    distances = ndef run_simulation(model):
    distances = np.linspace(1e3, 2.25e8, 20)

    f_before, f_after = [], []

    for d in distances:
        original = logical_zero()
        noisy = deep_space_noise(original.copy(), d)

        before = fidelity(original, noisy)

        features = extract_features(noisy)
        pred = model(torch.tensor(features, dtype=torch.float32))

        q, e = decode_prediction(pred)
        corrected = apply_correction(noisy, q, e)

        after = fidelity(original, corrected)

        f_before.append(before)
        f_after.append(after)

    return distances, f_before, f_after


9. MAIN


if _name_ == "_main_":
    print("Generating dataset...")
    X, y = generate_dataset(4000)

    print("Training model...")
    model = train_model(X, y)

    print("Running simulation...")
    d, before, after = run_simulation(model)

    print("Plotting results...")
    plt.plot(d, before, label="Without AI-QEC")
    plt.plot(d, after, label="With AI-QEC")

    plt.xlabel("Distance")
    plt.ylabel("Fidelity")
    plt.title("AI-Assisted Quantum Error Correction")
    plt.legend()

    plt.savefig("fidelity.png")
    plt.show()
