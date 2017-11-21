# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 08:48:19 2017

@author: MannyXu
"""

class Animal(object):
    def __init__(self, name):
        self.name = name
 
    def getInfo(self):
        print("This animal's name:", self.name)
 
    def sound(self):
        print("The sound of this animal goes?")
        
class Dog(Animal):
    def __init__(self, name, size):
        self.name = name
        self.__size = size
 
    def getInfo(self):
        print("This dog's name:", self.name) 
        print("This dog’s size:", self.__size)

dog = Dog('asf', 'small')
dog.sound()