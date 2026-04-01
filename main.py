import matplotlib.pyplot as plt
from src.simulation import run_simulation

if __name__ == "__main__":
    distances, f_before, f_after = run_simulation()

    plt.plot(distances, f_before, label="Without QEC")
    plt.plot(distances, f_after, label="With QEC")
    plt.xlabel("Distance (km)")
    plt.ylabel("Fidelity")
    plt.title("Deep Space Quantum Communication with QEC")
    plt.legend()

    plt.savefig("results/fidelity_plot.png")
    plt.show()
