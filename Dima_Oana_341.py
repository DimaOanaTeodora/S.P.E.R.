# Dima Oana - Teodora 341

from casadi import *
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import quad
from scipy.special import comb

# ------z(t) and ploting for i) and ii) ----------
def ploting(t, p, w, n, ex):
	targets = []
	curve = np.zeros((2, len(t)))

	for i in range(len(t)):
		for j in range(n):
			curve[ :,i] = p[ :,j] *  pow(t[i], j) * comb(n, j) * pow((1 - t[i]),(n - j)) + curve[ :,i] 

	if ex == 2:
		for k in range(len(w[0])):
			targets.append(list(w[:, k]))
		
	plt.figure()

	# plot the curve
	plt.plot(
		curve[0,:], #
		curve[1,:])

	if ex == 2:
		# plot coordinates
		plt.plot(
			p[:, 0],
			p[:, 1],
			'ro:')

		# plot the target
		targets = np.array(targets)

		plt.plot(
			targets[:, 0],
			targets[:, 1],
			marker='x')
	plt.grid()
	plt.show()
# -------------- i) ------------

#-----------Input----------------
t_points = np.arange(0, 1, 0.01) 
n=3
coordinates = np.array([[ 3, 6, 4], 
						[ 0, 9, 30]])
# -----------------------------
ploting(t_points, coordinates, None, n, 1 )

# ----------------ii) -------------------------------

def binomial_coefficient(a, b, c, d): 
	value1 = a * b * comb(c, b) * (1 - a) * (c - b) 
	value2 = a * d * comb(c, d) * (1 - a) * (c - d) 
	return value1 - value2
	
def integration(a, b, c):
	return quad(binomial_coefficient, 0, 1, args=(a, b, c))[0]
	
#-----------Input----------------
sol = Opti()
t = np.array([0, 0.51, 0.85])
w = np.array([[3, 7, 10], [1, 5, 2]])
#-----------------------------------

n = len(t)
p = sol.variable(2, n)
b = np.zeros((n, n))

for k in range(n):
	tk = t[k]
	for i in range(n):
		b[i, k] = pow(tk, i) * comb(n, i) * pow(1 - tk, n - i) 
	sol.subject_to((p @ b[:, k]) == w[: ,k])

obj = None
for i in range(n - 1):
    for j in range(n - 1):
        obj = mtimes(
				mtimes(transpose(np.subtract(p[:, i + 1], p[:, i])), 
								np.subtract(p[:, j + 1], p[:, j])
					),
            	mtimes(pow(n,2), integration(i , n, j))
			   )

sol.minimize(obj)
solver_options = {'ipopt': {'print_level': 0, 'sb': 'yes'}, 'print_time': 0}
sol.solver('ipopt', solver_options)
sol = sol.solve()
p = sol.value(p)
ploting(t_points, p, w, n, 2)