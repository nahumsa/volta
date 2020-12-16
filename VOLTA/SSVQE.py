####################
## Helper imports ##
####################
import numpy as np
from typing import Union
import textwrap
from functools import partial

import sys
sys.path.append('./')

####################
## Qiskit imports ##
####################
import qiskit
from qiskit import QuantumCircuit
from qiskit.aqua.operators import OperatorBase, ListOp, PrimitiveOp, PauliOp
from qiskit.aqua.operators import I, X, Y, Z
from qiskit.circuit.library import TwoLocal
from qiskit.aqua.components.optimizers import Optimizer
from qiskit.aqua import QuantumInstance
from qiskit.providers import BaseBackend

###################
## Local imports ##
###################
from VOLTA.Observables import sample_hamiltonian
from VOLTA.SWAPTest import measure_swap_test

################
## begin code ##
################

class SSVQE(object):
    """Subspace-search variational quantum eigensolver for excited states 
    algorithm class.

    Based on https://arxiv.org/abs/1810.09434

    """
    def __init__(self, 
                 hamiltonian: Union[OperatorBase, ListOp, PrimitiveOp, PauliOp],
                 ansatz: QuantumCircuit,
                 backend: Union[BaseBackend, QuantumInstance],
                 debug: bool=False):
        """Initialize the class.

        Args:
            hamiltonian (Union[OperatorBase, ListOp, PrimitiveOp, PauliOp]): Hamiltonian 
            constructed using qiskit's aqua operators.
            ansatz (QuantumCircuit): Anstaz that you want to run VQD.
            optimizer (qiskit.aqua.components.optimizers.Optimizer): Classical Optimizers 
            from aqua components.
            backend (Union[BaseBackend, QuantumInstance]): Backend for running the algorithm.
        """
        
        # Input parameters
        self.hamiltonian = hamiltonian        
        self.n_qubits = hamiltonian.num_qubits
        self.optimizer = optimizer
        self.backend = backend
        
        # Helper Parameters
        self.ansatz = ansatz
        self.n_parameters = self._get_num_parameters
        self._debug = debug
        
        #
        self._ansatz_1_params = None
        self._first_optimization = False

        # Running inate functions
        self._inate_optimizer_run()

    def _create_blank_circuit(self) -> list:
        return [QuantumCircuit(self.n_qubits) for _ in range(2**self.n_qubits)]

    def _copy_unitary(self, list_states: list) -> list:
        out_states = []
        for state in list_states:
            out_states.append(state.copy())
        return out_states
    
    def _apply_initialization(self, list_states: list) -> None:
        for ind, state in enumerate(list_states):
            b = bin(ind)[2:]
            if len(b) != self.n_qubits:
                b = '0'*(self.n_qubits - len(b)) + b
            spl = textwrap.wrap(b, 1)
            for qubit, val in enumerate(spl):
                if val == '1':
                    state.x(qubit)
    
    @property
    def _get_num_parameters(self) -> int:
        """Get the number of parameters in a given ansatz.

        Returns:
            int: Number of parameters of the given ansatz.
        """
        return len(self.ansatz.parameters)

    def _apply_varform_params(self, ansatz, params: list):
        """Get an hardware-efficient ansatz for n_qubits
        given parameters.
        """

        # Define variational Form
        var_form = ansatz

        # Get Parameters from the variational form
        var_form_params = sorted(var_form.parameters, key=lambda p: p.name)

        # Check if the number of parameters is compatible
        assert len(var_form_params) == len(params), "The number of parameters don't match"

        # Create a dictionary with the parameters and values
        param_dict = dict(zip(var_form_params, params))

        # Assing those values for the ansatz
        wave_function = var_form.assign_parameters(param_dict)

        return wave_function

    def _apply_ansatz(self, list_states: list, name: str=None) -> None:
        for states in list_states:
            if name:
                self.ansatz.name = name
            states.append(self.ansatz, range(self.n_qubits))
        
    # TODO
    def _construct_states(self):
        circuit = self._create_blank_circuit()
        self._apply_initialization(circuit)

        if self._first_optimization:
            self._apply_ansatz(circuit), 'U(ϕ)'
        
        if type(self._ansatz_1_params) != list:
            self._apply_ansatz(circuit)    
        
        else:
            self._apply_ansatz(circuit, 'V(θ)')
            for ind in range(len(circuit)):
                circuit[ind] = self._apply_varform_params(circuit[ind], self._ansatz_1_params)

        return circuit

    def _cost_function_1(self, params:list) -> float:
        """Evaluate the first cost function of SSVQE.

        Args:
            params (list): Parameter values for the ansatz.

        Returns:
            float: Cost function value.
        """

        # Construct states
        states = self._construct_states()
        
        cost = 0
        for state in states:
            qc = self._apply_varform_params(state, params)

            # Hamiltonian
            hamiltonian_eval = sample_hamiltonian(hamiltonian=self.hamiltonian, 
                                                 ansatz=qc, 
                                                 backend=self.backend)
            
            cost += hamiltonian_eval
        
        return cost

    def _inate_optimizer_run(self):
        
        # Random initialization
        params = np.random.rand(self.n_parameters)

        optimal_params, energy, n_iters = self.optimizer.optimize(num_vars=self.n_parameters, 
                                                                  objective_function=self._cost_function_1, 
                                                                  initial_point=params)
        
        self._ansatz_1_params = optimal_params
        self._first_optimization = True
    
    def _cost_excited_state(self, ind: int, params: list):
        cost = 0
        # Construct states
        states = self._construct_states()

        # Define Ansatz
        qc = self._apply_varform_params(states[ind], params)

        # Hamiltonian
        hamiltonian_eval = sample_hamiltonian(hamiltonian=self.hamiltonian, 
                                             ansatz=qc, 
                                             backend=self.backend)
        cost += hamiltonian_eval

        
        return - cost

    def _excited_state_optimizer(self, index) -> (float, QuantumCircuit):
        cost = partial(self._cost_excited_state, index)

        params = np.random.rand(self.n_parameters)

        optimal_params, energy, n_iters = optimizer.optimize(num_vars=self.n_parameters, 
                                                             objective_function=cost, 
                                                             initial_point=params)
        
        state = self._construct_states()[index]
        return energy, self._apply_varform_params(state, optimal_params)

    def run(self, index):
        energy, state = self._excited_state_optimizer(index)
        return energy, state

if __name__ == "__main__":
    from qiskit import BasicAer
    optimizer = qiskit.aqua.components.optimizers.COBYLA()

    backend = QuantumInstance(backend=BasicAer.get_backend('qasm_simulator'),
                    shots=10000)

    hamiltonian = (1/2*(Z^I) + 1/2*(Z^Z))
    ansatz = TwoLocal(hamiltonian.num_qubits, ['ry','rz'], 'cx', reps=1)
    algo = SSVQE(hamiltonian, ansatz, backend)
    print(algo._construct_states()[3])
    