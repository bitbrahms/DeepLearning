# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 08:41:53 2017

@author: MannyXu
"""
import matplotlib.pyplot as plt
fig, (ax0, ax1) = plt.subplots(2, 1)      # 2行1列
ax0.plot(range(7), [3, 4, 7, 6, 2, 8, 9], color = 'r', marker = 'o')
ax0.set_title('subplot1')    # 设置子图的标题
plt.subplots_adjust(hspace = 0.5)
ax1.plot(range(7), [5, 1, 8, 2, 6, 9, 4], color = 'green', marker = 'o')
ax1.set_title('subplot2')