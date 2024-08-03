import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
import time


def lattice_based_cryptography():
    lattice_basis = np.random.randint(-10, 10, size=(3, 3))
    shortest_vector = None
    min_length = float('inf')

    for i in range(lattice_basis.shape[0]):
        for j in range(lattice_basis.shape[1]):
            vector = lattice_basis[:, j]
            length = np.linalg.norm(vector)
            if length < min_length:
                min_length = length
                shortest_vector = vector

    return shortest_vector


def qkd_bb84_protocol(n_bits=8):
    max_qubits = 29  # Set a reasonable upper limit for the number of qubits
    n_bits = min(n_bits, max_qubits)

    backend = Aer.get_backend('qasm_simulator')

    alice_bits = np.random.randint(2, size=n_bits)
    alice_bases = np.random.randint(2, size=n_bits)
    bob_bases = np.random.randint(2, size=n_bits)

    qc = QuantumCircuit(n_bits, n_bits)
    for i in range(n_bits):
        if alice_bits[i] == 1:
            qc.x(i)
        if alice_bases[i] == 1:
            qc.h(i)
    qc.barrier()
    for i in range(n_bits):
        if bob_bases[i] == 1:
            qc.h(i)
        qc.measure(i, i)

    transpiled_qc = transpile(qc, backend)

    start_time = time.time()
    qobj = assemble(transpiled_qc)
    result = backend.run(qobj, shots=1).result()
    end_time = time.time()

    measured_bits = np.array([int(bit) for bit in list(result.get_counts(qc).keys())[0]])
    sifted_key = measured_bits[alice_bases == bob_bases]
    time_taken = end_time - start_time

    hacked = any(measured_bits != alice_bits)

    return alice_bits, alice_bases, bob_bases, measured_bits, sifted_key, hacked, time_taken


# Get number of bits from user input
n_bits = int(input("Enter the number of bits for Lattice vs BB84 (maximum 29): "))

# Example Usage
shortest_vector = lattice_based_cryptography()
alice_bits, alice_bases, bob_bases, measured_bits, sifted_key, hacked, time_taken = qkd_bb84_protocol(n_bits)

print("Shortest vector:", shortest_vector)
print("Alice's bits:   ", alice_bits)
print("Alice's bases:  ", alice_bases)
print("Bob's bases:    ", bob_bases)
print("Measured bits:  ", measured_bits)
print("Sifted key:     ", sifted_key)
print(f"Hacked:         {hacked}")
print(f"Time taken:     {time_taken} seconds")
