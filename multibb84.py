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
    
    correct_bits = (measured_bits == alice_bits).sum()
    hacked = correct_bits < (0.5 * n_bits)
    
    return alice_bits, alice_bases, bob_bases, measured_bits, sifted_key, hacked, time_taken

# Get number of bits from user input
try:
    n_bits = int(input("Enter the number of bits for Multivariate vs BB84 (maximum 29): "))
    if n_bits > 29:
        raise ValueError("Number of bits exceeds the maximum allowed (29). Using maximum value (29).")
except ValueError as e:
    print(e)
    n_bits = 29

# Example Usage
polynomials, variables = multivariate_polynomial(3, 2)
solutions = solve_multivariate(polynomials, variables)
alice_bits, alice_bases, bob_bases, measured_bits, sifted_key, hacked, time_taken = qkd_bb84_protocol(n_bits)

print("Polynomials:", polynomials)
print("Solutions:  ", solutions)
print("Alice's bits:", alice_bits)
print("Alice's bases:", alice_bases)
print("Bob's bases:", bob_bases)
print("Measured bits:", measured_bits)
print("Sifted key:", sifted_key)
print(f"Hacked:     {hacked}")
print(f"Time taken: {time_taken} seconds")
