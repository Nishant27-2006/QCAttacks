import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.circuit.library import QFT
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

def modular_exp(a, power, N):
    U = QuantumCircuit(4)
    for _ in range(power):
        U.swap(0, 1)
        U.swap(1, 2)
        U.swap(2, 3)
        U.swap(0, 1)
        U.swap(1, 2)
        U.swap(2, 3)
        if a == 7:
            U.swap(0, 3)
            U.swap(1, 2)
            U.swap(0, 2)
            U.swap(1, 3)
    return U

def qpe_amod15(a):
    n_count = 8
    qc = QuantumCircuit(4 + n_count, n_count)
    for q in range(n_count):
        qc.h(q)
    qc.x(3 + n_count)
    
    for q in range(n_count):
        qc.append(modular_exp(a, 2**q, 15).to_gate().control(), [q] + [i + n_count for i in range(4)])
    
    qc.append(QFT(n_count, inverse=True).to_gate(), range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc

def shors_algorithm(N):
    a = np.random.randint(2, N)
    while np.gcd(a, N) != 1:
        a = np.random.randint(2, N)
    qc = qpe_amod15(a)
    backend = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, backend)
    
    start_time = time.time()
    qobj = assemble(transpiled_qc)
    result = backend.run(qobj, shots=1024).result()
    end_time = time.time()
    
    counts = result.get_counts()
    time_taken = end_time - start_time
    return counts, time_taken

# Get N value from user input
try:
    N = int(input("Enter the N value for Multivariate vs Shor's Algorithm: "))
    if N < 2:
        raise ValueError("N must be greater than 1.")
except ValueError as e:
    print(e)
    N = 15

# Example Usage
polynomials, variables = multivariate_polynomial(3, 2)
solutions = solve_multivariate(polynomials, variables)
shors_counts, time_taken = shors_algorithm(N)
hacked = False  # As requested, setting hacked to False

print("Polynomials:", polynomials)
print("Solutions:  ", solutions)
print("Shor's Algorithm Counts:", shors_counts)
print(f"Hacked:                  {hacked}")
print(f"Time taken:              {time_taken} seconds")
