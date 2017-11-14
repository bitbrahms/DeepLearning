# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 09:33:04 2017

@author: MannyXu
"""

import scipy as sp
import pylab as pl
listA = sp.ones(500)
listA [100:300] = -1
f = sp.fft(listA)
pl.plot(f)