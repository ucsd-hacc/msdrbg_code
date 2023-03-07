This code demonstrates the SUS attack on maliciously-generated parameters for the RSA PRG, as described in our paper, ["On the Possibility of a Backdoor in the Micali-Schnorr Generator"](https://ia.cr/2023/TBD)

To carry out the SUS attack using the 1024-bit example parameters, run `sage sus_demo.py`.

To use larger parameters that were generated with undiscoverability in mind, comment out the "import smallparams as params" on line 102 and uncomment one of the following lines. Note that for the larger parameters instead of running LLL in sage, you'll be prompted for a filename to which the lattice will be written so that it can be reduced with an external tool, then you'll be prompted for a filename to read the reduced lattice from. (See the paper for runtime estimates.)

If you have magma installed, uncomment line 87 and comment out line 88 to use magma for the Groebner basis computation. (For the larger parameters, this will likely be faster.)
