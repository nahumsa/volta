# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


import numpy as np
from qiskit.opflow import OperatorBase


def classical_solver(hamiltonian: OperatorBase) -> (np.array, np.array):
    """Solves Classically the hamiltonian.

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
