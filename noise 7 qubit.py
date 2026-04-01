!pip install qiskit qiskit-aer matplotlib numpy

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error
import matplotlib.pyplot as plt
import numpy as np

def create_steane_code_circuit():
    qc = QuantumCircuit(7,7)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.cx(0,3)
    qc.cx(1,3)
    qc.cx(2,3)
    qc.cx(0,4)
    qc.cx(1,4)
    qc.cx(2,5)
    qc.cx(0,5)
    qc.cx(1,6)
    qc.cx(2,6)
    qc.barrier()
    qc.measure(range(7), range(7))
    return qc

qc_steane = create_steane_code_circuit()
qc_steane.draw("mpl")

noise_model = NoiseModel()
depol_error = depolarizing_error(0.05, 1)
bit_flip_error = pauli_error([('X',0.03),('I',0.97)])
phase_flip_error = pauli_error([('Z',0.03),('I',0.97)])

for gate in ["h"]:
    noise_model.add_all_qubit_quantum_error(depol_error, [gate])
    noise_model.add_all_qubit_quantum_error(bit_flip_error, [gate])
    noise_model.add_all_qubit_quantum_error(phase_flip_error, [gate])

for gate in ["cx"]:
    noise_model.add_all_qubit_quantum_error(depol_error, [gate])

print("Advanced Deep Space Noise Model Created")

simulator = Aer.get_backend("aer_simulator")
qc_t = transpile(qc_steane, simulator)
result = simulator.run(qc_t, noise_model=noise_model, shots=2048).result()
counts_steane = result.get_counts()
print("Counts with Steane QEC:", counts_steane)

plot_histogram(counts_steane)
plt.title("Steane Code under Deep Space Noise")
plt.show()

shots = 2048
logical_zero = '0'*7
fidelity_steane = counts_steane.get(logical_zero,0)/shots
print("Logical Qubit Fidelity with Steane QEC:", fidelity_steane)

qc_no_qec = QuantumCircuit(1,1)
qc_no_qec.h(0)
qc_no_qec.measure(0,0)
qc_no_qec_t = transpile(qc_no_qec, simulator)
result_no_qec = simulator.run(qc_no_qec_t, noise_model=noise_model, shots=2048).result()
counts_no_qec = result_no_qec.get_counts()
fidelity_no_qec = counts_no_qec.get("0",0)/shots

print("Counts without QEC:", counts_no_qec)
print("Fidelity without QEC:", fidelity_no_qec)

plt.bar(["With Steane QEC", "Without QEC"], [fidelity_steane, fidelity_no_qec])
plt.ylabel("Fidelity")
plt.title("Fidelity Comparison under Deep Space Noise")
plt.show()

plt.savefig("fidelity_comparison_advanced.png")
