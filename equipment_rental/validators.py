from datetime import datetime
from itertools import cycle
import re


def ci(ci):
	ci = ci.replace('.', '')

	if '-' not in ci:
		return False

	n, dv = ci.split('-')

	s = 0
	for x, y in zip(n[::-1], cycle(range(2,8))):
		s += int(x)*y

	m = 11 - s % 11
	if m == 11:
		m = '0'
	elif m == 10:
		m = 'K'
	else:
		m = str(m)

	return dv == m
