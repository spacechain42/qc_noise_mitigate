from mitiq.benchmarks import generate_rb_circuits
from mitiq.zne import execute_with_zne
from mitiq.zne.scaling import (
    fold_gates_at_random,
    fold_global,
    fold_all
)
from mitiq.zne.inference import LinearFactory, RichardsonFactory
from mitiq import (
    Calibrator,
    Settings,
    execute_with_mitigation,
    MeasurementResult,
)

from qiskit_ibm_runtime.fake_provider import FakeJakartaV2  # Fake (simulated) QPU


# Global settings for ZNE
n_qubits = 2
depth_circuit = 100
shots = 10**4

def execute_circuit(circuit):
    """Execute the input circuit and return the expectation value of |00..0><00..0|"""
    noisy_backend = FakeJakartaV2()
    noisy_result = noisy_backend.run(circuit, shots=shots).result()
    noisy_counts = noisy_result.get_counts(circuit)
    noisy_expectation_value = noisy_counts[n_qubits * "0"] / shots
    return noisy_expectation_value


qc = generate_rb_circuits(n_qubits, depth_circuit, return_type="qiskit")[0]
qc.measure_all()

zne_mitigated = execute_with_zne(qc, execute_circuit, factory=LinearFactory([1, 3, 5]))
unmitigated = execute_circuit(qc)
ideal = 1

print("ideal = \t \t", ideal)
print("unmitigated = \t \t", "{:.5f}".format(unmitigated))
print("ZNE mitigated = \t", "{:.5f}".format(zne_mitigated))
