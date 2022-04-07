# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:23:24 2021

"""
from casadi import *

import numpy as np
import numpy.matlib

from matplotlib import pyplot as plt

P={"A":np.array([[0.2718,   -0.8117],\
        [0.4666,  -0.7681],\
        [0.7449,    0.0175],\
        [-0.1182,    0.7736],\
        [-0.1704,    0.7547],\
        [-0.6283,    0.2834],
        [-0.7394,   -0.1424]]),\
   "b":np.matrix.transpose(np.array([0.5169, 0.4385, 0.6669, 0.6226, 0.6336, 0.7245, 0.6581])),\
   "V": [[-0.9688,  0.4089],\
                 [-0.7209,  -0.8783],\
                 [-0.2419,  -0.7179],\
                 [0.8958,  -0.0268],\
                 [0.8732,  0.9382],\
                 [-0.4757,  0.7321],\
                 [-0.8624,  0.6448]]}

# generate random linear cost
c=np.matrix.transpose(np.random.rand(2)-0.5)

# generate random quadratic cost
H=np.random.rand(2,2)
H=mtimes(H,np.matrix.transpose(H))
f=np.random.rand(2,1)-0.5
     
plotScaling=2
      
# construct the solver object, in which we store variables, parameters, cost and constraints
solver=Opti()

# define the variables to be used in the optimization problem
x=solver.variable(2,1); 

# define the constraints that appear in the optimization problem
solver.subject_to(mtimes(P["A"],x)<=P["b"])

# define the cost to be minimized
solver.minimize(mtimes(transpose(c),x))

# define properties for the ipopt solver (do not show intermediary info)
solver_options = {'ipopt': {'print_level': 0, 'sb': 'yes'}, 'print_time': 0}
solver.solver('ipopt', solver_options)

# run the solver and get the solution (if the problem is feasible of course)
sol = solver.solve()

# get the numerical value of the symbolic variable
xsol=sol.value(x)

#%% do the plotting

fig=plt.figure()
plt.title("solution of the LP problem")

ax = fig.add_subplot(1, 1, 1)
pgon = plt.Polygon(P["V"],color='g', alpha=0.5)
ax.add_patch(pgon)

a=[-2, 2, -2, 2]
plt.xlim(a[0:2])
plt.ylim(a[2:4])

plt.scatter(xsol[0], xsol[1], s=40, c='b')
plt.plot(a[0:2],\
         [((mtimes(transpose(c),xsol)-c[0]*a[0])/c[1]).full().reshape(-1,),\
          ((mtimes(transpose(c),xsol)-c[0]*a[1])/c[1]).full().reshape(-1,)])
           
plt.show(block=False)


#%% #################   the quadratic case   ################################

# construct the solver object, in which we store variables, parameters, cost and constraints
solver=Opti()

# define the variables to be used in the optimization problem
x=solver.variable(2,1); 

# define the constraints that appear in the optimization problem
solver.subject_to(mtimes(P["A"],x)<=P["b"]);

# define the cost to be minimized
solver.minimize(mtimes(mtimes(transpose(x),0.5*H),x)\
                +mtimes(transpose(f),x))

# define properties for the ipopt solver (do not show intermediary info)
solver_options = {'ipopt': {'print_level': 0, 'sb': 'yes'}, 'print_time': 0}
solver.solver('ipopt', solver_options)

# run the solver and get the solution (if the problem is feasible of course)
sol = solver.solve()

# get the numerical value of the symbolic variable
xsol=sol.value(x)

xunc=-mtimes(np.linalg.inv(H),f).full().reshape(-1,)

#%% do the plotting

fig=plt.figure()
plt.title("solution of the LP problem")

ax = fig.add_subplot(1, 1, 1)
pgon = plt.Polygon(P["V"],color='g', alpha=0.5)
ax.add_patch(pgon)

a=[-2, 2, -2, 2]
plt.xlim(a[0:2])
plt.ylim(a[2:4])

plt.scatter(xsol[0], xsol[1], s=40, c='b')
plt.scatter(xunc[0], xunc[1], s=40, c='r')

scaling=np.sqrt(mtimes(transpose(xsol-xunc),mtimes(0.5*H,xsol-xunc)))
L=np.linalg.cholesky(H)
theta=np.linspace(0,2*np.pi,100)

points=mtimes(np.linalg.inv(L),\
            transpose(np.concatenate((scaling*np.cos(theta),\
            scaling*np.sin(theta)),1)))+\
            np.matrix.transpose(np.matlib.repmat(xunc,len(theta),1))

plt.plot(points[0:1,:].full().reshape(-1,), points[1:2,:].full().reshape(-1,))
 
plt.show(block=False)








