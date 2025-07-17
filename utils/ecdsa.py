import utils.bashToy as bT
import secrets
import os

n = 18446744080022336321

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
	print(f"🔑 clave privada generada en : data/claves/clavePrivada.txt")

def escribirClavePublica(Q):
	with open("data/claves/clavePublica.txt", "w") as f:
		f.write(f'{Q[0]}\n{Q[1]}\n{Q[2]}')
	print(f"🔑 clave pública generada en : data/claves/clavePublica.txt")

def generarClaveECDSA(G, a, p):
	#Clave privada
	d = secrets.randbelow(n - 1) + 1
	#Clave pública
	Q = multiplicarPuntos(d, G, a, p)

	escribirClavePrivada(d)
	escribirClavePublica(Q)

def obtenerLlavePrivada():
	with open('data/claves/clavePrivada.txt', 'r') as llavePrivada:
		d = int(llavePrivada.read())
	return d

def obtenerLlavePublica():
	with open('data/claves/clavePublica.txt', 'r') as contenido:
		x = int(contenido.readline().strip())
		y = int(contenido.readline().strip())
		z = int(contenido.readline().strip())
	return [x, y ,z]

def obtenerKParaFirmar(G, a, p, z, d):
	while True:
		k = secrets.randbelow(n - 1) + 1
		R = multiplicarPuntos(k, G, a, p)
		r = R[0] % n
		if r == 0:
			continue
		try:
			inversoK = pow(k , -1, n)
		except ValueError:
			continue
		s = (inversoK * ( z + d * r)) % n
		if s == 0:
			continue
		break
	return [r,s]

def guardarFirma(firma, ruta):
	nombreArchivo = os.path.basename(ruta)
	nombre = os.path.splitext(nombreArchivo)[0]
	with open(f"data/firmas/{nombre}-Firma.txt", "w") as f:
		f.write(f'{firma[0]}\n{firma[1]}')
	print(f'Firma guardada en : data/firmas/{nombre}-Firma.txt')

def firmarMensaje(msj, G, a, p, ruta):
	d = obtenerLlavePrivada()
	msjStr = msj.decode('utf-8', errors='ignore')
	#Mensaje hasheado, de hexadecimal a entero
	z = int(bT.hashToy(msjStr), 16)
	#Para evitar valores de 0 en s o r, verificaremos
	firmar = obtenerKParaFirmar(G, a, p, z, d)
	guardarFirma(firmar, ruta)

def obtenerFirma(ruta):
	with open(ruta, 'r') as contenido:
		r = int(contenido.readline().strip())
		s = int(contenido.readline().strip())
	return [r,s]

def verificar(msj, G, a, p, ruta):
	firma = obtenerFirma(ruta)
	Q = obtenerLlavePublica()
	msjStr = msj.decode('utf-8', errors='ignore')
	z = int(bT.hashToy(msjStr), 16)
	w = pow(firma[1], -1, n)
	u1 = (z * w) % n
	u2 = (firma[0] * w) % n
	uG = multiplicarPuntos(u1, G, a, p)
	uQ = multiplicarPuntos(u2, Q, a, p)
	P = sumaPuntos(uG, uQ, a, p)
	r = P[0] % n
	if r == firma[0]:
		return '✅ Verificación válida'
	else:
		return '❌ Verificación no válida'




