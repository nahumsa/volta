####################
## Helper imports ##
####################
import numpy as np

####################
## Qiskit imports ##
####################
import qiskit
from qiskit.aqua.operators import OperatorBase, ListOp, PrimitiveOp, PauliOp
from qiskit.aqua.operators import I, X, Y, Z
from qiskit.circuit.library import TwoLocal

###################
## Local imports ##
###################
from utils import classical_solver
from Observables import *
from SWAPTest import measure_swap_test

################
## begin code ##
################

# hamiltonian = 1/2*((I^Z) + (Z^I) + 2*( (X^X) + (Y^Y)))
hamiltonian = 1/2*((Z^I) + (Z^Z))

eigenvalues = classical_solver(hamiltonian)
print(f"Eigenvalues: {eigenvalues}")

class VQD(object):
    """Variational Quantum Deflation algorithm

    """
    def __init__(self, n_qubits: int, n_excited_states: int, beta: float,
                 optimizer: qiskit.aqua.components.optimizers.Optimizer, 
                 backend: qiskit.providers.BaseBackend,
                 num_shots: int=10000):
        """Initialize the class.

        Args:
            n_qubits (int): Number of qubits to use with the hardware efficient ansatz.
            n_excited_states (int): Number of excited states that you want to find the energy.
            beta (float): Strenght parameter for the swap test.
            optimizer (qiskit.aqua.components.optimizers.Optimizer): Classical Optimizers 
            from aqua components.
            backend (qiskit.providers.BaseBackend): Backend for running the algorithm.
            num_shots (int): Number of shots. (Default: 10000)
        """
        
        # Input parameters
        self.n_qubits = n_qubits        
        self.optimizer = optimizer
        self.backend = backend
        self.NUM_SHOTS = num_shots
        self.BETA = beta
        
        # Helper Parameters
        self.n_excited_states = n_excited_states
        self.n_parameters = self._get_num_parameters(self.n_qubits)
        self.ansatz = self._get_ansatz(n_qubits)
        # Logs
        self._states = []
        self._energies = []

    @property
    def energies(self):
        """ Returns a list with energies.

        Returns:
            list: list with energies
        """
        return self._energies
    
    @property
    def states(self):
        """ Returns a list with states associated with each energy.

        Returns:
            list: list with states.
        """
        return self._states

    def _get_ansatz(self, n_qubits):
        return TwoLocal(n_qubits, ['ry','rz'], 'cx', reps=1)

    def _get_num_parameters(self, n_qubits):
        return len(self.ansatz.parameters)

    def _get_varform_params(self, params):
        """Get an hardware-efficient ansatz for n_qubits
        given parameters.
        """

        # Define variational Form
        var_form = self.ansatz

        # Get Parameters from the variational form
        var_form_params = sorted(var_form.parameters, key=lambda p: p.name)

        # Check if the number of parameters is compatible
        assert len(var_form_params) == len(params), "The number of parameters don't match"

        # Create a dictionary with the parameters and values
        param_dict = dict(zip(var_form_params, params))

        # Assing those values for the ansatz
        wave_function = var_form.assign_parameters(param_dict)

        return wave_function
    
    def get_hamiltonian(self, qc: qiskit.QuantumCircuit, 
                        backend: qiskit.providers.BaseBackend, 
                        num_shots: int):
        """Get the hamiltonian that we want to minimize.

        Args:
            qc (qiskit.QuantumCircuit): Ansatz with pararamers attached.
            backend (qiskit.providers.BaseBackend): Backend to run.
            num_shots (int): Number of shots.
        """
        # Hamiltonian BCS
        # hamiltonian = .5*(measure_iz(qc, backend, num_shots) + measure_zi(qc, backend, num_shots)
        #                + 2*(measure_xx(qc, backend, num_shots) + measure_yy(qc, backend, num_shots)))

        hamiltonian = 0.5*(measure_zi(qc, backend, num_shots) + measure_zz(qc, backend, num_shots))
        return hamiltonian
    
    def energy_evaluation(self, params):
        
        # Define Ansatz
        qc = self._get_varform_params(params)

        # Hamiltonian
        hamiltonian = self.get_hamiltonian(qc, self.backend, self.NUM_SHOTS)
        
        # Fidelity
        fidelity = 0.
        if len(self.states) != 0:
            for state in self.states:
                fidelity += measure_swap_test(qc, state, self.backend, self.NUM_SHOTS)

        # Get the cost function
        cost = hamiltonian + self.BETA*fidelity
        
        return cost

    def optimizer_run(self):

        params = np.random.rand(self.n_parameters)

        optimal_params, energy, n_iters = self.optimizer.optimize(num_vars=self.n_parameters, 
                                                                    objective_function=self.energy_evaluation, 
                                                                    initial_point=params)
        
        # Logging the energies and states
        # TODO: Change to an ordered list.
        
        self._energies.append(energy)
        self._states.append(self._get_varform_params(optimal_params))
    
    

##############        
## End code ##
##############