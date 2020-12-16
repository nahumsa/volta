# import sys
# sys.path.append('../')

# import unittest

# # Qiskit imports
# import qiskit
# from qiskit.circuit.library import TwoLocal
# from qiskit import QuantumCircuit, BasicAer
# from qiskit.aqua import QuantumInstance
# from qiskit.aqua.operators import Z,I

# # Local Imports
# from VOLTA.SSVQE import SSVQE
# from VOLTA.utils import classical_solver

# class TestVQD(unittest.TestCase): 

#     def setUp(self):

#         optimizer = qiskit.aqua.components.optimizers.COBYLA()
        
#         backend = QuantumInstance(backend=BasicAer.get_backend('qasm_simulator'),
#                           shots=10000)
           
#         hamiltonian = (1/2*(Z^I) + 1/2*(Z^Z))
#         ansatz = TwoLocal(hamiltonian.num_qubits, ['ry','rz'], 'cx', reps=2)

#         self.Algo = SSVQE(hamiltonian=hamiltonian,
#                           ansatz = ansatz,
#                           optimizer=optimizer,
#                           backend=backend)

#         self.Algo.run(verbose=0)        
#         self.eigenvalues, _ = classical_solver(hamiltonian)
        
    
#     def test_energies(self): 
#         want = self.eigenvalues[0]
#         got = self.Algo.energies[0]
#         decimalPlace = 1
#         message = "SSVQE not working for the ground state of 1/2*((Z^I) + (Z^Z))"
#         self.assertAlmostEqual(want, got, decimalPlace, message)
        
#         decimalPlace = 1
#         want = self.eigenvalues[1]
#         got = self.Algo.energies[1]
#         message = "SSVQE not working for the first excited state of 1/2*((Z^I) + (Z^Z))"
#         self.assertAlmostEqual(want, got, decimalPlace, message)
    

# if __name__== "__main__":
#     unittest.main(argv=[''], verbosity=2, exit=False);