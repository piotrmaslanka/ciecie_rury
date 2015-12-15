"""
Generates a test example
"""
from __future__ import division

import random

fname = raw_input('Pass file name')
stocksize = int(raw_input('Pass stock size'))
elems = int(raw_input('Pass amount of elements'))

genmin = lambda: int((random.random() * 0.55 + 0.05) * stocksize)

of = open(fname, 'w')
of.write('%s\n%s\n' % (stocksize, elems))

for _ in xrange(elems):
    of.write('%s\n' % (genmin(),))

of.close()
