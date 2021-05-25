import numpy as np

from typing import Union

from qiskit.opflow import I, X, Y, Z
from qiskit.opflow.list_ops.summed_op import SummedOp
from qiskit.opflow.primitive_ops.pauli_op import PauliOp


def listop2op(listop: list, coef: float = 1) -> PauliOp:
    """Creates aqua operator from a list of aqua operators.

    Args:
        listop (list): List of aqua operators.
        coef (float, optional): Coefficient that multiplies the operator.
        Defaults to 1.

    Returns:
        PauliOp: aqua operator.
    """
    for i, val in enumerate(listop):
        if i == 0:
            op = val
        else:
            op = op ^ val

    return coef * op


def create_epsilons(epsilons: list) -> SummedOp:
    """Creates epsilon part of the BCS Hamiltonian.

    Args:
        epsilons (list): Epsilons for the BCS Hamiltonian.

    Returns:
        SummedOp: Epsilon part of the BCS Hamiltonian.
    """
    op = 0
    for ind, eps in enumerate(epsilons):
        aux = [I] * len(epsilons)
        aux[ind] = Z
        op += listop2op(aux, eps)
    return op


def BCS_hamiltonian(epsilons: Union[list, np.array], V: float) -> SummedOp:
    """Creates the BCS Hamiltonian given epsilons and V.

    Args:
        epsilons (Union[list,np.array]): Epsilons for the BCS hamiltonian.
        V (float): V for the BCS Hamiltonian.

    Returns:
        SummedOp: BCS Hamiltonian.
    """
    if type(epsilons) != type(np.array([])):
        epsilons = np.array(epsilons)

    hamiltonian = create_epsilons(epsilons / 2)
    hamiltonian += V * (
        1 / 2 * (listop2op([X] * len(epsilons)))
        + 1 / 2 * (listop2op([Y] * len(epsilons)))
    )
    return hamiltonian
