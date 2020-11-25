import qiskit
from qiskit import QuantumCircuit, execute
from typing import Union
from qiskit.aqua import QuantumInstance
from qiskit.providers import BaseBackend

def swap_test_circuit(qc1: QuantumCircuit, qc2: QuantumCircuit) -> QuantumCircuit:
    """ Construct the SWAP test circuit given two circuits.

    Args:
        qc1(qiskit.QuantumCircuit): Quantum circuit for the 
        first state.
        qc2(qiskit.QuantumCircuit): Quantum circuit for the 
        second state.
    Output:
        (qiskit.QuantumCircuit): swap test circuit.
    """
    # Helper variables
    n_total = qc1.num_qubits + qc2.num_qubits
    range_qc1 = [i + 1 for i in range(qc1.num_qubits)]
    range_qc2 = [i + qc1.num_qubits + 1 for i in range(qc2.num_qubits)]

    # Constructing the SWAP test circuit
    qc_swap = QuantumCircuit(n_total + 1, 1)
    qc_swap.append(qc1, range_qc1)
    qc_swap.append(qc2, range_qc2)
    
    # Swap Test
    qc_swap.h(0)
    for index, qubit in enumerate(range_qc1):
        qc_swap.cswap(0, qubit, range_qc2[index] )
    qc_swap.h(0)
    
    # Measurement on the auxiliary qubit
    qc_swap.measure(0,0)
    return qc_swap

def measure_swap_test(qc1: QuantumCircuit, qc2: QuantumCircuit,
                     backend: Union[BaseBackend,QuantumInstance],
                     num_shots: int=10000) -> float:
    """ Returns the fidelity from a SWAP test.
    """
    swap_circuit = swap_test_circuit(qc1, qc2)

    # Check if the backend is a quantum instance.
    if qiskit.aqua.quantum_instance.QuantumInstance == type(backend):
        count = backend.execute(swap_circuit).get_counts()
    else:
        count = execute(swap_circuit, backend=backend, shots=num_shots).result().get_counts()
    
    if '0' not in count:
        count['0'] = 0
    if '1' not in count:
        count['1'] = 0

    total_counts = count['0'] + count['1'] 
    fid_meas = count['0']
    p_0 = fid_meas / total_counts
    return 2*(p_0 - 1/2)