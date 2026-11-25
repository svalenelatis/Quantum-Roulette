from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
#from scipy.stats import chisquare
import random

class QuantumRNG:
    def __init__(self,size,sim = True):
        self.size = size # amount of bits the QRNG will hold for random generation
        self.bank = []
        self.sim = sim
        self.waiting = True
        self._refresh_bank()

    def _get_bit_string(self,amt):
        #internal helper to generate a bitstring via the quantum circuit
        circ = QuantumCircuit(amt,amt)
        circ.h(range(amt))
        circ.measure(range(amt),range(amt))
        if self.sim:
            backend = AerSimulator()
        else:
            pass
            backend = AerSimulator()
            #TODO run on actual IBM backend for final project
        job = backend.run(circ,shots=1)
        results = job.result()
        return list(dict(results.get_counts()).keys())[0] #format result to bitstring


    def _refresh_bank(self):
        delta = self.size - len(self.bank)
        bstring = self._get_bit_string(delta)
        for b in bstring:
            self.bank.append(b)
        self.waiting = False


    def random(self, i1=0,i2=8):
        #implements the Lumbroso's Fast Dice Roller algorithm with bits from the bank
        # i2 HAS to be a positive integer, and i1 has to be less than i2
        if i1 > i2:
            raise ValueError("Failed random draw. The first argument must be less than the second.")
        v = 1
        c = 0
        #first, normalize range to 0
        delta = i1
        n = i2 - delta + 1
        #we're now generating a random value from 0 to n
        #Lumbroso's Fast Dice Roller
        while(True):
            if (not self.bank):
                #print("Bank ran out mid-roll, regenerating...")
                self._refresh_bank()
                #print("New bank acquired: ",self.bank)
            b = self.bank.pop()
            #print("Drew a ",b)
            v = 2*v
            c = 2*c + int(b)
            if(v >= n): #if our possible states is at, or exceeds, our ceiling
                if(c < n): #if we have a valid value
                    #print(f"Accepted {c}, returning {c+delta}")
                    return c + delta #return with removed delta
                #print(f"Rejecting value. v: {v}, c: {c}, ceiling: {ceiling}") #if no balid value, reject and roll-down
                v -= n
                c -= n


"""
q = QuantumRNG(20,True)
#print(q.bank)
results = {}
test = 10
results = {str(x+1): 0 for x in range(test)}
times = 10000
for x in range(times):
    result = q.random(1,test)
    results[str(result)] += 1

print(results)
probability = {k: v/times for k,v in results.items()}
print(probability)

# compare chisquare test of random values
vals = {str(x+1): 0 for x in range(test)}
for x in range(times):
    vals[str(random.randint(1,test))] += 1
print(chisquare(list(vals.values())))

print(chisquare(list(results.values())))
"""
