import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 2)
        )

    def forward(self, x):
        return self.net(x)

def get_features(state):
    return np.abs(state[:6])

def generate_data(encode_fn, noise_fn, samples=2000):
    X, y = [], []
    distances = [500, 384400, 225_000_000]

    for _ in range(samples):
        theta = np.random.rand() * np.pi
        phi = np.random.rand() * 2 * np.pi
        q = np.array([
            np.cos(theta/2),
            np.exp(1j*phi) * np.sin(theta/2)
        ])

        encoded = encode_fn(q)
        d = np.random.choice(distances)

        noisy = encoded.copy()
        for i in range(3):
            noisy[i*2:(i+1)*2] = noise_fn(noisy[i*2:(i+1)*2], d)

        X.append(get_features(noisy))
        y.append(1 if d > 100000 else 0)

    return np.array(X), np.array(y)

def train_ai(X, y):
    model = Decoder()
    opt = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    X_t = torch.tensor(X, dtype=torch.float32)
    y_t = torch.tensor(y, dtype=torch.long)

    for epoch in range(50):
        opt.zero_grad()
        out = model(X_t)
        loss = loss_fn(out, y_t)
        loss.backward()
        opt.step()

    return model
