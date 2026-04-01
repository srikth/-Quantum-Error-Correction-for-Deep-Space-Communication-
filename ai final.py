import torch
import torch.nn as nn

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
import numpy as np
from qec.steane import logical_zero
from qec.error_models import apply_pauli

def extract_features(state):
    return np.concatenate([np.real(state), np.imag(state)])

def generate_dataset(N=4000):
    X, y = [], []

    for _ in range(N):
        state = logical_zero()
        noisy = state.copy()

        label = 0

        if np.random.rand() < 0.7:
            qubit = np.random.randint(0,7)
            error = np.random.choice(['X','Y','Z'])
            noisy = apply_pauli(noisy, qubit, error)

            error_map = {'I':0,'X':1,'Y':2,'Z':3}
            label = qubit * 4 + error_map[error]

        X.append(extract_features(noisy))
        y.append(label)

    return np.array(X), np.array(y)
import torch
import torch.optim as optim
from ai.model import QuantumDecoder

def train(X, y):
    model = QuantumDecoder()

    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y, dtype=torch.long)

    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(50):
        optimizer.zero_grad()
        output = model(X_t)
        loss = loss_fn(output, y_t)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    return model
