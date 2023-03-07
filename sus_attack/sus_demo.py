from sage.all import *
import random
import mvcoppersmith

x = polygen(ZZ)

def RSAPRG(s0, N, e, k):
	state = s0
	for i in range(50000):
		state = Integer(pow(state, e, N))
		yield (state % 2**k)

def attempt(diylll=True, mult=1, extras=[]):
	#global prg,full,outputs,fullstates,which_outputs,bs,fss,ys,F,M,unknown_parts,scalefactors,ms,ML,I,IB,polys
	N = p*q
	s0 = randint(1,N-1)
	print("Generating PRG outputs")
	prg = RSAPRG(s0=Integer(s0), N=N, e=e, k=k)
	full = RSAPRG(s0=Integer(s0), N=N, e=e, k=int(log(N,2)+1))
	howfar = max(a for (a,_) in relation_coeffs)+1
	outputs = [next(prg) for _ in range(howfar)]
	fullstates = [next(full) for _ in range(howfar)]
	print("Outputs generated")

	print("---attack starts here---")
	which_outputs = [i for (i,c) in relation_coeffs]

	bs = [outputs[i] for i in which_outputs]
	#fss = [fullstates[i] for i in which_outputs] # for debugging
	#unknown_parts = [(fs-b)//(2**k) for (fs,b) in zip(fss,bs)] # for debugging

	ys = polygens(ZZ,'y',len(bs))
	F = (Integer(pow(2,-(len(ys)//2)*k,p)) * (
		prod(
			(2**k * ys[i] + bs[i])**(relation_coeffs[i][1])
			for i in range(len(relation_coeffs))
			if relation_coeffs[i][1] > 0
		)
		- prod(
			(2**k * ys[i] + bs[i])**(-relation_coeffs[i][1])
			for i in range(len(relation_coeffs))
			if relation_coeffs[i][1] < 0
		)
	)) % p

	#assert F(*[(fs - b)//(2**k) for (b,fs) in zip(bs,fss)]) % p == 0 # for debugging

	print("Making Coppersmith lattice...")
	mvcoppersmith.coppersmith_params(F, mult=mult, extras=extras)
	M, ms, scalefactors = mvcoppersmith.coppersmith_makelattice(F, N//(2**k), p, mult=mult, extras=extras)
	print("detM = 2^", prod(M.diagonal()).nbits())

	#assert all(mvcoppersmith.vec_to_poly(vec,ms,scalefactors)(*unknown_parts) % p**mult == 0 for vec in M) # for debugging

	assert not any(M[i].is_zero() for i in range(len(ms)))

	if diylll:
		filename = input("Output filename for lattice to be LLL-reduced: ")
		mvcoppersmith.export_lattice(M, filename)

		filename = input("Input filename for LLL-reduced lattice: ")
		ML = mvcoppersmith.import_lattice(filename)
	else:
		print("Running LLL on dimension %d lattice..." % len(M.rows()))
		ML = M.dense_matrix().LLL()
		print("Done running LLL.")

	global shortrows
	shortrows = [row for row in ML.rows() if row.norm(1) < p**mult]
	print("Number of vectors that seem short enough: ", len(shortrows))
	if len(shortrows) == 0: return False
	polys = [mvcoppersmith.vec_to_poly(row, ms, scalefactors) for row in shortrows]
	#assert all( pol(*unknown_parts) == 0 for pol in polys)

	# polys now contains polynomials that evaluate to 0 over the integers at the solution.
	# The coefficients are huge (on the order of p^mult), but the solutions we're looking for are (relatively) small.
	# We can dramatically speed up the groebner basis computation by working mod a prime instead of over ZZ.
	if 'grob_mod' in params.hints:
		grob_mod = params.hints['grob_mod']
	else:
		print("Finding prime to work mod (if slow, this can be precomputed)")
		grob_mod = next_prime(2 * N//(2**k)) # slow
	grob_ring = Zmod(grob_mod)
	I = ideal([f.change_ring(grob_ring) for f in polys])
	print("Taking Groebner basis")
	set_verbose(2)
	#IB = I.groebner_basis(algorithm='magma') # uncomment if magma is installed
	IB = I.groebner_basis() # comment out if magma is installed
	results = [(poly / poly.content()).univariate_polynomial() for poly in IB if poly.nvariables() == 1]
	if len(results) == 0:
		print("no results")
	for poly in results:
		print(poly)
		root = poly.roots(multiplicities=False)[0]
		if poly.variables()[0] == ys[0]:
			recovered_state = bs[0] + 2**k * (root.lift())
			if recovered_state == fullstates[which_outputs[0]]:
				print("Successfully recovered full state %d!" % which_outputs[0])
	return results

if __name__ == "__main__":
	import smallparams as params
	#import mediumparams as params
	#import largeparams as params
	#import hugeparams as params
	e,p,q,N,k,f,relation_coeffs = params.e, params.p, params.q, params.N, params.k, params.f, params.relation_coeffs

	print("p is", p.nbits(), "bits")
	print("q is", q.nbits(), "bits")
	print("N is", N.nbits(), "bits")
	print("Size of unknown part is", N.nbits() - k, "bits")

	mult = params.hints['mult'] if 'mult' in params.hints else 1
	diylll = params.hints['diylll'] if 'diylll' in params.hints else True
	attempt(mult=mult, extras=[], diylll=diylll)
