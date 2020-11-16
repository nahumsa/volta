import numpy as np
import qiskit
from qiskit.aqua.operators import OperatorBase, ListOp, PrimitiveOp, PauliOp
from qiskit.aqua.operators import I, X, Y, Z
from utils import classical_solver
from qiskit.circuit.library import TwoLocal
from Observables import *

# hamiltonian = 1/2*((I^Z) + (Z^I) + 2*( (X^X) + (Y^Y)))
hamiltonian = 1/2*((Z^I) + (Z^Z))

eigenvalues = classical_solver(hamiltonian)
print(f"Eigenvalues: {eigenvalues}")

class VQD(object):
    """Variational Quantum Deflation algorithm

    """
    def __init__(self, n_qubits: int, 
                 optimizer: qiskit.aqua.components.optimizers.Optimizer, 
                 backend: qiskit.providers.BaseBackend):
        """Initialize the class.

        Args:
            n_qubits (int): Number of qubits to use with the hardware efficient ansatz.
            optimizer (qiskit.aqua.components.optimizers.Optimizer): 
            Classical Optimizers from aqua components.
            backend (qiskit.providers.BaseBackend): Backend for running the algorithm.
        """

        self.n_qubits = n_qubits
        self.ansatz = self._get_ansatz(n_qubits)
        self.optimizer = optimizer
        self.backend = backend
        self.states = []
        self.energies = []
        self.NUM_SHOTS = 10000

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
        
        # Get the cost function
        cost = hamiltonian
        print(cost)
        return cost

    def optimizer_run(self):
        n_parameters = self._get_num_parameters(self.n_qubits)

        params = np.random.rand(n_parameters)

        optimal_params, energy, n_iters = self.optimizer.optimize(num_vars=n_parameters, 
                                                                    objective_function=self.energy_evaluation, 
                                                                    initial_point=params)
        print(energy)
