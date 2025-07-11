def x(m, P, Q,  p):
	x3 = (pow(m, 2) - P[0] - Q[0]) % p
	return x3

def y(m, P, x3, p):
	y3= (m*(P[0] - x3) - P[1]) % p
	return y3

def dobladoPuntos(P, Q, a, p):
	salida = []
	m = (((3 * pow(P[0], 2)) + a) * (pow(2 * P[1], -1, p))) % p
	x3 = x(m, P, Q, p)
	salida = [x3, y(m, P, x3, p)]
	return salida

def puntosDiferentes(P, Q, p):
	salida = []
	m = ((Q[1] - P[1]) * (pow(Q[0] - P[0] ,-1 ,p))) % p
	x3 = x(m, P, Q, p)
	salida = [x3, y(m, P, x3, p)]
	return salida

#P = [x1,y1,z1] y Q = [x2,y2,z2]
def sumaPuntos(P, Q, a, p):
	#Cuando es Fi
	if P[0] == Q[0] and P[1] != Q[1]:
		return ['O','O']
	#Para doblado de puntos
	elif P[0] == Q[0] and P[1] == Q[1]:
		return dobladoPuntos(P, Q, a, p)
	#Para putos diferentes
	else:
		return puntosDiferentes(P, Q, p)

