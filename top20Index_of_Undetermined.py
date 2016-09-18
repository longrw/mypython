#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gzip
import sys
import time

time1 = time.time()
d = dict()
indexs = [head.strip().split(":")[9] for head in gzip.open('/haplox/users/longrw/Undetermined_Index/' + sys.argv[1], 'r') if head.startswith("@NS500713")]
index_uniqs = set(indexs)
for index in index_uniqs:
    d[index] = indexs.count(index)
d_sort = sorted(d.items(), key = lambda x:x[1], reverse = True)
for top20 in d_sort[:20]:
    print top20
time2 = time.time()
print 'Time used: ' + str(time2 - time1)
