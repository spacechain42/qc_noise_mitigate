from qiskit.circuit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeNairobiV2
from qiskit.visualization import plot_distribution
import mitiq

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = FakeNairobiV2()
job = backend.run(qc, shots=100)
dist = plot_distribution(job.result().get_counts())

dist.savefig('src/dist.png')
