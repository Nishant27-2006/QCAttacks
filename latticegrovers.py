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

def grovers_algorithm(num_qubits, target_state):
    max_qubits = 29  # Set a reasonable upper limit for the number of qubits
    num_qubits = min(num_qubits, max_qubits)
    
    circuit = QuantumCircuit(num_qubits)
    circuit.h(range(num_qubits))
    
    oracle = QuantumCircuit(num_qubits)
    for qubit in range(num_qubits):
        if target_state[qubit] == '0':
            oracle.x(qubit)
    oracle.cz(0, num_qubits - 1)
    for qubit in range(num_qubits):
        if target_state[qubit] == '0':
            oracle.x(qubit)
    
    diffuser = QuantumCircuit(num_qubits)
    diffuser.h(range(num_qubits))
    diffuser.x(range(num_qubits))
    diffuser.cz(0, num_qubits - 1)
    diffuser.x(range(num_qubits))
    diffuser.h(range(num_qubits))
    
    circuit.append(oracle.to_gate(), range(num_qubits))
    circuit.append(diffuser.to_gate(), range(num_qubits))
    circuit.measure_all()
    
    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(circuit, backend)
    
    start_time = time.time()
    result = backend.run(transpiled_circuit, shots=128).result()  # Reduced shots to 128 for faster execution
    end_time = time.time()
    
    counts = result.get_counts()
    time_taken = end_time - start_time
    
    total_counts = sum(counts.values())
    max_count = max(counts.values())
    hacked = max_count < (0.5 * total_counts)
    
    return counts, hacked, time_taken

# Get target state from user input
target_state = input("Enter the target state for Lattice vs Grover's Algorithm: ")
if len(target_state) > 29:
    print("Target state length exceeds the maximum allowed (29). Using the first 29 characters.")
    target_state = target_state[:29]

# Example Usage
shortest_vector = lattice_based_cryptography()
grovers_counts, hacked, time_taken = grovers_algorithm(len(target_state), target_state)

print("Shortest vector:", shortest_vector)
print("Grover's Algorithm Counts:", grovers_counts)
print(f"Hacked:                   {hacked}")
print(f"Time taken:               {time_taken} seconds")
