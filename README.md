# Quantum Cryptography and Cyber Attacks

This project investigates the effectiveness of various quantum cryptographic methods against different quantum attacks. The encryption methods used are Quantum Key Distribution (QKD), Lattice-Based Cryptography, and Multivariate Cryptography. The attack methods are BB84 Protocol, Shor's Algorithm, and Grover's Algorithm.

## Setup Instructions

### Prerequisites

Ensure you have Python 3.8 or higher installed. You will also need to install the necessary Python libraries.

### Libraries to Install

Use the following commands to install the required libraries:

```sh
pip install qiskit sympy numpy
Running the Scripts
There are nine scripts, each testing a different combination of encryption and attack methods. Follow the instructions below to run each script.

Script 1: QKD vs BB84
python
Copy code
python script1_qkd_bb84.py
Input
Enter the number of bits for QKD vs BB84 (maximum 29).
Script 2: QKD vs Shor's Algorithm
python
Copy code
python script2_qkd_shor.py
Input
Enter the N value for Shor's Algorithm.
Script 3: QKD vs Grover's Algorithm
python
Copy code
python script3_qkd_grover.py
Input
Enter the target state for Grover's Algorithm.
Script 4: Lattice vs BB84
python
Copy code
python script4_lattice_bb84.py
Input
Enter the number of bits for Lattice vs BB84 (maximum 29).
Script 5: Lattice vs Shor's Algorithm
python
Copy code
python script5_lattice_shor.py
Input
Enter the N value for Lattice vs Shor's Algorithm.
Script 6: Lattice vs Grover's Algorithm
python
Copy code
python script6_lattice_grover.py
Input
Enter the target state for Lattice vs Grover's Algorithm.
Script 7: Multivariate vs BB84
python
Copy code
python script7_multivariate_bb84.py
Input
Enter the number of bits for Multivariate vs BB84 (maximum 29).
Script 8: Multivariate vs Shor's Algorithm
python
Copy code
python script8_multivariate_shor.py
Input
Enter the N value for Multivariate vs Shor's Algorithm.
Script 9: Multivariate vs Grover's Algorithm
python
Copy code
python script9_multivariate_grover.py
Input
Enter the target state for Multivariate vs Grover's Algorithm.
Example Data Sets to Use
For each encryption method, use the following data sets in ascending order of data size:

"Hello Quantum"
"Quantum computing is a rapidly evolving field. Its potential to solve complex problems faster than classical computers is a topic of extensive research and excitement"
[1, 2, 3, 4, 5]
list(range(100)) (generates a list with random numbers from 1-100 for 100 elements)
{"index": i, "binary": bin(i), "factors": [j for j in range(1, i) if i % j == 0]} for i in range(1, 100)
These data sets should be used as inputs for the respective scripts to test the effectiveness of each encryption method against the attack methods.

Interpreting Results
Each script will output the following:

Encryption method details (e.g., Alice's bits, bases, etc.).
Attack method details (e.g., measured bits, counts, etc.).
Whether the encryption was hacked (True or False).
Time taken for the process.
Contributing
Feel free to contribute to this project by adding new encryption and attack methods or improving the existing scripts.
