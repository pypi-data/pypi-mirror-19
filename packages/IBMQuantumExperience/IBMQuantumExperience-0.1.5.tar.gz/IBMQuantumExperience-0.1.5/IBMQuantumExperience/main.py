from IBMQuantumExperience import IBMQuantumExperience

api = IBMQuantumExperience("admin@ibm.quantum.com", "7N75G\\c!", {"url": 'https://qcwi-develop.mybluemix.net/api'})
qasm = 'IBMQASM 2.0;\n\ninclude "qelib1.inc";\nqreg q[5];\ncreg c[5];\nh q[0];\ncx q[0],q[2];\nmeasure q[0] -> c[0];\nmeasure q[2] -> c[1];\n'
result = api.runExperiment(qasm, 'real', 1)
print(result)
codeid = result['idCode']
code = api.getImageCode(codeid)
print(code)