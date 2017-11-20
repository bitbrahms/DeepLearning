# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 09:22:22 2017

@author: MannyXu
"""

import numpy as np
import pylab as pl

x = np.linspace(-np.pi, np.pi, 256)
s = np.sin(x)
c = np.cos(x)
pl.title('Trig')
pl.xlabel('X')
pl.ylabel('Y')
pl.plot(x,s)
pl.plot(x,c)

