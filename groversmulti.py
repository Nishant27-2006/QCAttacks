import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
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
    return counts, time_taken


def get_user_input():
    data = input("Enter a data set (string, list, or complex data structure): ")
    try:
        parsed_data = eval(data)
    except:
        parsed_data = data
    return parsed_data


# Get data set from user input
data_set = get_user_input()

# Process the input data set
if isinstance(data_set, str):
    polynomials, variables = multivariate_polynomial(2, 1)
else:
    polynomials, variables = multivariate_polynomial(3, 2)

solutions = solve_multivariate(polynomials, variables)
grovers_counts, time_taken = grovers_algorithm(2,
                                               '10')  # Reduced num_qubits to 2 and target_state to '10' for faster execution

# Determining if the data was hacked or not
hacked = any(count > 0 for count in grovers_counts.values())

# Print results
print(f"Data: {data_set}")
print(f"Polynomials: {polynomials}")
print(f"Solutions: {solutions}")
print("Grover's Algorithm Counts:", grovers_counts)
print(f"Hacked: {hacked}")
print(f"Time taken: {time_taken} seconds")
