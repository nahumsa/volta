import unittest
from qiskit import QuantumCircuit, BasicAer
from qiskit.utils import QuantumInstance
from volta.swaptest import measure_swap_test, measure_dswap_test


class TestSWAPTest(unittest.TestCase):
    def setUp(self):
        self.qc1 = QuantumCircuit(1)
        self.qc1.x(0)
        self.qc2 = QuantumCircuit(1)
        # self.backend = BasicAer.get_backend("qasm_simulator")
        self.backend = QuantumInstance(
            backend=BasicAer.get_backend("qasm_simulator"), shots=10000
        )

    def test_10states(self):
        want = 0.0
        got = measure_swap_test(self.qc2, self.qc1, self.backend)
        decimalPlace = 1
        message = "Swap test not working for states 0 and 1."
        self.assertAlmostEqual(want, got, decimalPlace, message)

    def test_01states(self):
        want = 0.0
        got = measure_swap_test(self.qc1, self.qc2, self.backend)
        decimalPlace = 1
        message = "Swap test not working for states 0 and 1."
        self.assertAlmostEqual(want, got, decimalPlace, message)

    def test_00states(self):
        want = 1.0
        got = measure_swap_test(self.qc2, self.qc2, self.backend)
        decimalPlace = 2
        message = "Swap test not working for states 0 and 0."
        self.assertAlmostEqual(want, got, decimalPlace, message)

    def test_11states(self):
        want = 1.0
        got = measure_swap_test(self.qc1, self.qc1, self.backend)
        decimalPlace = 2
        message = "Swap test not working for states 1 and 1."
        self.assertAlmostEqual(want, got, decimalPlace, message)


class TestDestructiveSWAPTest(unittest.TestCase):
    def setUp(self):
        self.qc1 = QuantumCircuit(1)
        self.qc1.x(0)
        self.qc2 = QuantumCircuit(1)
        # self.backend = BasicAer.get_backend("qasm_simulator")
        self.backend = QuantumInstance(
            backend=BasicAer.get_backend("qasm_simulator"), shots=10000
        )

    def test_10states(self):
        want = 0.0
        got = measure_dswap_test(self.qc2, self.qc1, self.backend)
        decimalPlace = 1
        message = "Swap test not working for states 0 and 1."
        self.assertAlmostEqual(want, got, decimalPlace, message)

    def test_01states(self):
        want = 0.0
        got = measure_dswap_test(self.qc1, self.qc2, self.backend)
        decimalPlace = 1
        message = "Swap test not working for states 0 and 1."
        self.assertAlmostEqual(want, got, decimalPlace, message)

    def test_00states(self):
        want = 1.0
        got = measure_dswap_test(self.qc2, self.qc2, self.backend)
        decimalPlace = 2
        message = "Swap test not working for states 0 and 0."
        self.assertAlmostEqual(want, got, decimalPlace, message)

    def test_11states(self):
        want = 1.0
        got = measure_dswap_test(self.qc1, self.qc1, self.backend)
        decimalPlace = 2
        message = "Swap test not working for states 1 and 1."
        self.assertAlmostEqual(want, got, decimalPlace, message)


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)