This repo contains example code to accompany our paper ["On the Possibility of a Backdoor in the Micali-Schnorr Generator"](https://ia.cr/2023/440)

`nothing_up_my_sleeve.py` verifies the "Nothing up my sleeve" parameters for the Bad-e attack on MS PRG from section A.4.

`example_eSP.py` verifies that the example parameters for the eSP attack on RSA PRG do produce partially-hidden cycles as described in section 5.3.1.

`example_SUS.py` verifies that some example parameters for the SUS attack on RSA PRG to give rise to the desired relation between PRG states, as described in section 5.3.2

The `sus_attack/` directory contains code to carry out the full SUS attack on maliciously-generated RSA PRG parameters of various sizes.
