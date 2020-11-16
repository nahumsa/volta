from qiskit.circuit.library import TwoLocal

def _get_ansatz(n_qubits):
    return TwoLocal(n_qubits, ['ry','rz'], 'cx', reps=1)

def get_num_parameters(n_qubits):
    return len(_get_ansatz(n_qubits).parameters)

def get_var_form(params, n_qubits=2):
    """Get an hardware-efficient ansatz for n_qubits
    given parameters.
    """
    
    # Define variational Form
    var_form = _get_ansatz(n_qubits)
    
    # Get Parameters from the variational form
    var_form_params = sorted(var_form.parameters, key=lambda p: p.name)
    
    # Check if the number of parameters is compatible
    assert len(var_form_params) == len(params), "The number of parameters don't match"
    
    # Create a dictionary with the parameters and values
    param_dict = dict(zip(var_form_params, params))
    
    # Assing those values for the ansatz
    wave_function = var_form.assign_parameters(param_dict)
    
    return wave_function