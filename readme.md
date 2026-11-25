Are you upset by the idea that your online roulette games are powered by fake, deterministic random chance, derived easily by knowing the starting state?

Look no further than QRNG Quantum Roulette!!

By utilizing the true randomness of quantum states, we can create a truly random string of bits, and therefore almost any truly random quantum effect (factoring in environment noise and imperfections in quantum circuits)

Wthin random_module.py, you'll find the code implementing the quantum circuit (x qubit -> hadamard gates, measured and mapped to x classical bits) to generate a random bit string, called the 'bank'.

Next, we use Lumbroso's Fast Dice Roller algorithm to convert the bank of bits into random values, preserving entropy and rolling down if our value gets too big.

Lastly, we pump the values into a quickly designed roulette Pygame, found in quantRoulette.py

To play Quantum Roulette, make sure your python environment has qiskit and pygame installed on it- check requirements.txt for the right pygame version. Then, bet away with truly random (sort of) outcomes!

TODO for this project
Adding async bank retrieval, for when connected to a real IBM quantum backend
Needs to connect to the actual IBM backend
Measurements to prove actual uniformity of distribution against Mersenne Twister approach
Better roulette game
Better graphics
Quantum Log In into IBM backend
