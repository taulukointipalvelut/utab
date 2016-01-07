# -*- coding: utf-8 -*-

def bitshiftadd(bits, bit, shift):

	return (bit << shift) | bits

def xbit(bits, x):

	return (bits>>x)&1

def lastbit(bits):

	return bits&1

def eachbit(bits):
	for i in range(20):
		yield (bits>>i)&1