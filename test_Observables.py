import unittest
import qiskit
from qiskit import BasicAer
from Observables import *
from Observables import sample_hamiltonian
from qiskit.aqua.operators import I, X, Y, Z
import numpy as np

class TestObservables(unittest.TestCase): 
    def setUp(self):
        # Simulator
        self.backend = BasicAer.get_backend("qasm_simulator")
        
        # ZZ expectation value of 1
        self.qcZ = qiskit.QuantumCircuit(2)        
        
        # XX expectation value of 1
        self.qcX = qiskit.QuantumCircuit(2)        
        self.qcX.h(range(2))
        
        # YY expectation value of 1
        self.qcY = qiskit.QuantumCircuit(2)        
        self.qcY.h(range(2))
        self.qcY.s(range(2))
        
        
    def test_ZZ(self): 
        want = 1.
        # got = measure_zz(self.qcZ, self.backend)
        hamiltonian = (Z^Z)
        got = sample_hamiltonian(hamiltonian, self.backend, self.qcZ)
        decimalPlace = 2
        message = "ZZ measurement not working for state Zero^Zero."
        self.assertAlmostEqual(want, got, decimalPlace, message)
    
    def test_XX(self): 
        want = 1.
        # got = measure_xx(self.qcX, self.backend)
        hamiltonian = (X^X)
        got = sample_hamiltonian(hamiltonian, self.backend, self.qcX)
        decimalPlace = 2
        message = "XX measurement not working for state Plus^Plus."
        self.assertAlmostEqual(want, got, decimalPlace, message)
    
    def test_YY(self): 
        want = 1.
        # got = measure_yy(self.qcY, self.backend)
        hamiltonian = (Y^Y)
        got = sample_hamiltonian(hamiltonian, self.backend, self.qcY)
        decimalPlace = 2
        message = "YY measurement not working for state iPlus^iPlus."
        self.assertAlmostEqual(want, got, decimalPlace, message)

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False);