#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gzip
import sys
import time

time1 = time.time()
for index in sorted(head.strip().split(":")[9] for head in gzip.open('/haplox/users/longrw/Undetermined_Index/' + sys.argv[1], 'r') if head.startswith("@NS500713")):
    print index
time2 = time.time()
print 'Time used: ' + str(time2 - time1)
