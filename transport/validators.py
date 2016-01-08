from datetime import datetime
from itertools import cycle
import re

def plate(plate):
	if re.match('[A-Z]{2}[0-9]{4}|[B-DF-HJ-NP-TV-Z]{4}[0-9]{2}', plate.upper()):
		return True
	else:
		return False

def year(year):
	return year >= 1990 and year <= datetime.now().year + 1

def ci(ci):
	ci = ci.replace('.', '')
	n, dv = ci.split('-')

	s = 0
	for x, y in zip(n[::-1], cycle(range(2,8))):
		s += int(x)*y

	m = 11 - s%11
	if m == 11:
		m = '0'
	elif m == 10:
		m = 'K'
	else:
		m = str(m)

	return dv == m