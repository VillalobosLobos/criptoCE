import utils.bashToy as bT
import secrets

def x(m, P, Q,  p):
	x3 = (pow(m, 2) - P[0] - Q[0]) % p
	return x3

def y(m, P, x3, p):
	y3= (m*(P[0] - x3) - P[1]) % p
	return y3

def dobladoPuntos(P, Q, a, p):
	#En caso de que Z sea Fi
	if P[2] == 0:
		return [0, 1, 0]
	#Para y = 0
	if P[1] == 0:
		return [0, 1, 0]

	salida = []
	m = (((3 * pow(P[0], 2)) + a) * (pow(2 * P[1], -1, p))) % p
	x3 = x(m, P, Q, p)
	salida = [x3, y(m, P, x3, p), 1]
	return salida

def puntosDiferentes(P, Q, p):
	#Si P es Fi, regresame Q
	if P[2] == 0:
		return Q
	#si Q es Fi, regresame P
	if Q[2] == 0:
		return P

	salida = []
	m = ((Q[1] - P[1]) * (pow(Q[0] - P[0] ,-1 ,p))) % p
	x3 = x(m, P, Q, p)
	salida = [x3, y(m, P, x3, p), 1]
	return salida

#P = [x1,y1,z1] y Q = [x2,y2,z2]
def sumaPuntos(P, Q, a, p):
	#Para z=0
	if P[2] == 0:
		return Q
	#Para y=0
	if Q[2] == 0:
		return P

	#Cuando es Fi
	if P[0] == Q[0] and P[1] != Q[1]:
		return [0, 1, 0]
	#Para doblado de puntos
	elif P[0] == Q[0] and P[1] == Q[1]:
		return dobladoPuntos(P, Q, a, p)
	#Para putos diferentes
	else:
		return puntosDiferentes(P, Q, p)

#Usando el algoritmo double-and-add
def multiplicarPuntos(k, P, a, p):
	#Para nuestro Fi/ infinito
	if k == 0:
		return [0, 1, 0]
	if k == 1:
		return P
	#Para valores negativos de k
	if k < 0:
		P_neg = [P[0], (-P[1]) %p, P[2]]
		return multiplicarPuntos(-k, P_neg, a, p)

	resultado = [0, 1, 0]
	base = P

	while k > 0:
		if k & 1: #Para el bit menos significativo
			resultado = sumaPuntos(resultado, base, a, p)
		base = dobladoPuntos(base, base, a, p)
		k >>= 1 #Para dividir k entre 2 (binario)
	return resultado

def escribirClavePrivada(d):
	with open("data/claves/clavePrivada.txt", "w") as f:
		f.write(f'{d}')

def escribirClavePublica(Q):
	with open("data/claves/clavePublica.txt", "w") as f:
		f.write(f'{Q}\n')

def generarClaveECDSA(G, a, p):
	n = 18446744080022336321
	#Clave privada
	d = secrets.randbelow(n - 1) + 1
	#Clave pública
	Q = multiplicarPuntos(d, G, a, p)

	escribirClavePrivada(d)
	escribirClavePublica(Q)

def firmarMensaje():
	pass




