#-*- coding:utf-8 -*-
'''
Created on 2020年12月24日

@author: My
'''

import numpy as np

x=np.array([1,2,3,4,5,6])
print(x)
print(x.dtype)

print(np.zeros(6))
print(np.zeros((2,3)))
x=np.array([[1,2],[3,4],[5,6]])

print(np.ones((2,3)))
print(np.empty((2,3)))
print(np.arange(1,9))

print(x)
print(x.shape)
print(x.ndim)

print(x.dtype)

int_arry=np.array([1,2,3,4],dtype=np.int64)
print(int_arry)
float_arry=int_arry.astype(np.float64)
print(float_arry)

x=np.array([[1,2],[3,4],[5,6]])
print(x)
print(x[0][1])
print(x[0,1])
print(x[1:2])

x=np.array([3,2,3,1,3,0])
print(x)

y=np.array([True,False,True,False,True,False])
print(y)
print(y.dtype)
print(x[y])
print(x[y==False])

print(x[x>1])

x=np.array([1,2,3,4,5,6])
print(x)
print(x[[0,2,2]])
print(x[[-1,-2,-3]])


k=np.arange(9)
print(k)
m=k.reshape((3,3))
print(m)
print(m.T)
print(np.dot(m,m.T))

x=np.array([[1,4],[6,7],[8,9]])
print(x)

print(x.mean(axis=1))