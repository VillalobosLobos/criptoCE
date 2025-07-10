#Esta función nos servira para pasar de cadena a bytes
def aBytes(cadenas):
	salida = []
	for cadena in cadenas:
		salida.append(cadena.encode())
	return salida

#Hacemos xor por cada bit de nuestro bytes
def xor(cadenas):
	cadenas = aBytes(cadenas)
	resultado = []
	for i in range(8):
		xorByte = 0
		for palabra in cadenas: 
			xorByte ^= palabra[i]
		resultado.append(xorByte)
	resultado = bytes(resultado)
	return resultado.hex()

#Sirve para agregar espacios en caso de que falten para los 8 bytes
def rellenado(cadena):
	if len(cadena[len(cadena)-1]) < 8:
		espacio = 8 - len(cadena[len(cadena)-1]) 
		cadena[len(cadena)-1] = cadena[len(cadena)-1] + (espacio * " ")
	return cadena

#Para separar en bloques de 8 bytes
def bloques(cadena):
	salida=[]
	for i in range(0, len(cadena), 8):
		salida.append(cadena[i:i+8])
	salida = rellenado(salida)
	salida = xor(salida)
	return salida

def hashToy(cadena):
	digesto = bloques(cadena)
	return digesto

