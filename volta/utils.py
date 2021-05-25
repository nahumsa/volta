import numpy as np
from qiskit.opflow import OperatorBase

def classical_solver(hamiltonian: OperatorBase) -> np.array:
    """ Solves Classically the hamiltonian.

    Args:
        hamiltonian (qiskit.aqua.operators.OperatorBase): Hamiltonian that you want to
        get the eigenvalues.

    Returns:
        np.array: Eigenvalues of the hamiltonian.
    """
    
    try:
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.to_matrix())
    
    except:
        raise Exception("Not able to get the eigenvalues.")

    return eigenvalues, eigenvectors