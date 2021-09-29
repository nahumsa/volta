# volta

[![build and test](https://github.com/nahumsa/volta/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/nahumsa/volta/actions/workflows/build.yaml)

This is a library that I started developing to create faster workflows, firstly for variational quantum algorithms, using qiskit. 

The main feature is the `volta.observables.sample_hamiltonian` which enables you to do easy evaluation of the expectation value for a hamiltonian defined using `opflow` and a quantum circuit.

I plan to implement Hamiltonian Simulation algorithms as well as noise mitigation for this package.

## Variational Quantum Algorithms

- Variational Quantum Deflation based on https://arxiv.org/abs/1805.08138.
- Subspace-search variational quantum eigensolver for excited states based on https://arxiv.org/abs/1810.09434. 

## SWAP test

- SWAP test using controlled swaps;
- Destructive SWAP test;

## Hamiltonian Simulation

## Error Mitigation
