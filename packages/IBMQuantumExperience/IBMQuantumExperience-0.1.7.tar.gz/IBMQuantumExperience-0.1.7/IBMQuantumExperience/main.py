from IBMQuantumExperience import IBMQuantumExperience

#api = IBMQuantumExperience("erespia2@gmail.com", "24500qTa", {'url': 'https://qcwi-develop.mybluemix.net/api'})
#api = IBMQuantumExperience("demo@demo.com", "demo1234QBITS")
api = IBMQuantumExperience("erespia2@gmail.com", "24500qTa")
#qasm = 'IBMQASM 2.0;\n\ninclude "qelib1.inc";\nqreg q[5];\ncreg c[5];\nh q[0];\ncx q[0],q[2];\nmeasure q[0] -> c[0];\nmeasure q[2] -> c[1];\n'
'''qasm = 'include \"qelib1.inc\";\nqreg q[5];\ncreg c[5];\nh q[0];\nh q[2];\ns q[2];\n'
result = api.runExperiment(qasm, 'sim', 1)
print(result)
codeid = result['idCode']
code = api.getImageCode(codeid)
print(code)'''

codes = api.getLastCodes()
for c in codes:
    for execution in c['executions']:
        print(execution['status'])