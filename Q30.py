#!/usr/bin/env python
#-*- coding:utf-8 -*-
import gzip
import sys
import time

time1 = time.time()
m, n, q20, q30 = 0, 0, 0, 0
for line in gzip.open(sys.argv[1]):
    m += 1
    if m % 4 == 0:
        n += len(line.strip())
        for i in line.strip():
            if ord(i) - 33 >= 20:
                q20 += 1
            if ord(i) - 33 >= 30:
                q30 += 1
time2 = time.time()
print 'read number: %s\nbase number: %s\nbase number(q20): %s\nbase number(q30): %s' % (m / 4, n, q20, q30)
print 'Q20: %.4f' % (float(q20) / float(n))
print 'Q30: %.4f' % (float(q30) / float(n))
print 'Time used: %s' % str(time2 - time1)
