from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def cifrarAESGCM(ruta):
	with open(ruta, "rb") as f:
		datos = f.read()

	#Generar clave de 128 bits (16 bytes)
	clave = os.urandom(16)

	#Generar nonce de 12 bytes
	nonce = os.urandom(12)

	#Crear objeto AESGCM
	aesgcm = AESGCM(clave)

	#Cifrar los datos
	textoCifrado = aesgcm.encrypt(nonce, datos, associated_data=None)

	#Recuerda que el tag ya está incluido al final del texto cifrado
	return textoCifrado, clave, nonce

def descifrarAESGCM(textoCifrado, clave, nonce, rutaSalida):
	#Crear objeto AESGCM
	aesgcm = AESGCM(clave)

	#Descifrar
	try:
		datosDescifrados = aesgcm.decrypt(nonce, textoCifrado, associated_data=None)
	except Exception as e:
		print("¡Error al descifrar! Posible manipulación o clave incorrecta.")
		raise e

	#Guardar resultado
	with open(rutaSalida, "wb") as f:
		f.write(datosDescifrados)



