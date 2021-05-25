import sys
sys.path.append('../')

import unittest

# Qiskit imports
import qiskit
from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit, BasicAer
from qiskit.utils import QuantumInstance
from qiskit.opflow import Z,I

# Local Imports
from volta.ssvqe import SSVQE
from volta.utils import classical_solver

# class TestSSVQD(unittest.TestCase): 

#     def setUp(self):

#         optimizer = qiskit.algorithms.optimizers.COBYLA()
        
#         backend = QuantumInstance(backend=BasicAer.get_backend('qasm_simulator'),
#                           shots=10000)
           
#         hamiltonian = (1/2*(Z^I) + 1/2*(Z^Z))
#         ansatz = TwoLocal(hamiltonian.num_qubits, ['ry','rz'], 'cx', reps=2)

#         self.Algo = SSVQE(hamiltonian=hamiltonian,
#                           ansatz = ansatz,
#                           optimizer=optimizer,
#                           backend=backend)

#         self.energy = []
#         self.energy.append(self.Algo.run(index=0)[0])
#         self.energy.append(self.Algo.run(index=1)[0])
#         self.eigenvalues, _ = classical_solver(hamiltonian)
        
    
#     def test_energies(self): 
#         want = self.eigenvalues[0]
#         got = self.energy[0]
#         decimalPlace = 1
#         message = "SSVQE not working for the ground state of 1/2*((Z^I) + (Z^Z))"
#         self.assertAlmostEqual(want, got, decimalPlace, message)
        
#         decimalPlace = 1
#         want = self.eigenvalues[1]
#         got = self.energy[1]
#         message = "SSVQE not working for the first excited state of 1/2*((Z^I) + (Z^Z))"
#         self.assertAlmostEqual(want, got, decimalPlace, message)
    

if __name__== "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False);