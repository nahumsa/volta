import unittest
import qiskit


from qiskit.circuit.library import TwoLocal
from qiskit import BasicAer
from qiskit.utils import QuantumInstance
from qiskit.opflow import Z, I


from volta.vqd import VQD
from volta.utils import classical_solver


class TestVQDSWAP(unittest.TestCase):
    def setUp(self):
        optimizer = qiskit.algorithms.optimizers.COBYLA()
        # backend = BasicAer.get_backend("qasm_simulator")
        backend = QuantumInstance(
            backend=BasicAer.get_backend("qasm_simulator"), shots=10000
        )

        hamiltonian = 1 / 2 * (Z ^ I) + 1 / 2 * (Z ^ Z)
        ansatz = TwoLocal(hamiltonian.num_qubits, ["ry", "rz"], "cx", reps=2)

        self.Algo = VQD(
            hamiltonian=hamiltonian,
            ansatz=ansatz,
            n_excited_states=1,
            beta=1.0,
            optimizer=optimizer,
            backend=backend,
        )

        self.Algo.run(verbose=0)
        self.eigenvalues, _ = classical_solver(hamiltonian)

    def test_energies_0(self):
        decimal_place = 1
        want = self.eigenvalues[0]
        got = self.Algo.energies[0]

        message = (
            "VQD with SWAP not working for the ground state of 1/2*((Z^I) + (Z^Z))"
        )
        self.assertAlmostEqual(want, got, decimal_place, message)

    def test_energies_1(self):
        decimal_place = 1
        want = self.eigenvalues[1]
        got = self.Algo.energies[1]

        message = "VQD with SWAP not working for the first excited state of 1/2*((Z^I) + (Z^Z))"
        self.assertAlmostEqual(want, got, decimal_place, message)


class TestVQDDSWAP(unittest.TestCase):
    def setUp(self):
        optimizer = qiskit.algorithms.optimizers.COBYLA()
        # backend = BasicAer.get_backend("qasm_simulator")
        backend = QuantumInstance(
            backend=BasicAer.get_backend("qasm_simulator"), shots=10000
        )

        hamiltonian = 1 / 2 * (Z ^ I) + 1 / 2 * (Z ^ Z)
        ansatz = TwoLocal(hamiltonian.num_qubits, ["ry", "rz"], "cx", reps=1)

        self.Algo = VQD(
            hamiltonian=hamiltonian,
            ansatz=ansatz,
            n_excited_states=1,
            beta=1.0,
            optimizer=optimizer,
            backend=backend,
            dswap=True,
        )

        self.Algo.run(verbose=0)
        self.eigenvalues, _ = classical_solver(hamiltonian)

    def test_energies_0(self):
        decimal_place = 1
        want = self.eigenvalues[0]
        got = self.Algo.energies[0]

        self.assertAlmostEqual(
            want,
            got,
            decimal_place,
            "VQD with DSWAP not working for the ground state of 1/2*((Z^I) + (Z^Z))",
        )

    def test_energies_1(self):
        decimal_place = 1
        want = self.eigenvalues[1]
        got = self.Algo.energies[1]

        self.assertAlmostEqual(
            want,
            got,
            decimal_place,
            "VQD with DSWAP not working for the first excited state of 1/2*((Z^I) + (Z^Z))",
        )


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)
