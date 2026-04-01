import numpy as np
import matplotlib.pyplot as plt
from ai.dataset import generate_dataset
from ai.train import train
from simulation.pipeline import run_trial

print("Generating dataset...")
X, y = generate_dataset()

print("Training model...")
model = train(X, y)

print("Running simulation...")

distances = np.linspace(1e3, 2.25e8, 20)

before, after = [], []

for d in distances:
    f1, f2 = run_trial(model, d)
    before.append(f1)
    after.append(f2)

plt.plot(distances, before, label="Without AI-QEC")
plt.plot(distances, after, label="With AI-QEC")

plt.xlabel("Distance")
plt.ylabel("Fidelity")
plt.legend()

plt.savefig("results/fidelity.png")
plt.show()
