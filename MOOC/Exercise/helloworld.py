# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:21:30 2017

@author: manny
"""

# Filename: helloworld.py
import wx 
class Frame1(wx.Frame):
   def __init__(self,parent,title):
        wx.Frame.__init__(self, parent, title = title, pos = (100,200), size = (200,100))
        panel = wx.Panel(self)
        text1 = wx.TextCtrl(panel, value = "Hello, World!", size = (200,100))
        self.Show(True)
if __name__ == '__main__': 
    app = wx.App()
    frame = Frame1(None, "Example")
    app.MainLoop()