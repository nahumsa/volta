from typing import Union
import qiskit
import numpy as np
from qiskit import Aer, execute
from qiskit.aqua.utils.backend_utils import is_aer_provider
from qiskit.aqua.operators import (PauliExpectation, CircuitSampler, ExpectationFactory,
                                   CircuitStateFn, StateFn, ListOp)

import sys
sys.path.append('../')

def sample_hamiltonian(hamiltonian: qiskit.aqua.operators.OperatorBase,
                       backend: Union[qiskit.providers.BaseBackend, qiskit.aqua.QuantumInstance],
                       ansatz: qiskit.QuantumCircuit):
    
    if qiskit.aqua.quantum_instance.QuantumInstance == type(backend):
        sampler = CircuitSampler(backend, param_qobj=is_aer_provider(backend.backend))
    else:
        sampler = CircuitSampler(backend)
        
    expectation = ExpectationFactory.build(operator=hamiltonian,backend=backend)
    observable_meas = expectation.convert(StateFn(hamiltonian, is_measurement=True))
    
    ansatz_circuit_op = CircuitStateFn(ansatz)
    
    expect_op = observable_meas.compose(ansatz_circuit_op).reduce()
    sampled_expect_op = sampler.convert(expect_op)
    
    return np.real(sampled_expect_op.eval())
