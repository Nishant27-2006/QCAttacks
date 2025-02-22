import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from sympy import symbols, solve
import time

def multivariate_polynomial(n, m):
    variables = symbols(f'x0:{n}')
    polynomials = []
    for _ in range(m):
        equation = sum(np.random.randint(-5, 5) * variables[i] * variables[j] for i in range(n) for j in range(n))
        polynomials.append(equation)
    return polynomials, variables

def solve_multivariate(polynomials, variables):
    solutions = solve(polynomials, variables)
    return solutions

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
target_state = input("Enter the target state for Multivariate vs Grover's Algorithm: ")
if len(target_state) > 29:
    print("Target state length exceeds the maximum allowed (29). Using the first 29 characters.")
    target_state = target_state[:29]

# Example Usage
polynomials, variables = multivariate_polynomial(3, 2)
solutions = solve_multivariate(polynomials, variables)
grovers_counts, hacked, time_taken = grovers_algorithm(len(target_state), target_state)

print("Polynomials:", polynomials)
print("Solutions:  ", solutions)
print("Grover's Algorithm Counts:", grovers_counts)
print(f"Hacked:                   {hacked}")
print(f"Time taken:               {time_taken} seconds")

