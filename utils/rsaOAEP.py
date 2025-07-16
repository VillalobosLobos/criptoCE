from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import base64

def generarClavesRSA(bits=2048):
	clavePrivada = rsa.generate_private_key(
		public_exponent=65537,
		key_size=bits
	)
	clavePublica = clavePrivada.public_key()

	#Exportamos ambas en base64 y las guardamos
	pemPriv = clavePrivada.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption()
	)

	pemPub = clavePublica.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)

	#Guardamos los archivos
	with open("data/claves/rsaPrivada.pem", "wb") as f:
		f.write(base64.b64encode(pemPriv))

	with open("data/claves/rsaPublica.pem", "wb") as f:
		f.write(base64.b64encode(pemPub))

def cifrarAESRSA(rutaLlavePublica, claveAES):
	with open(rutaLlavePublica, "rb") as f:
		llavePublicaDatos = base64.b64decode(f.read())

	llavePublica = serialization.load_pem_public_key(llavePublicaDatos)

	cifrado = llavePublica.encrypt(
		claveAES,
		padding.OAEP(
		mgf=padding.MGF1(algorithm=hashes.SHA256()),
		algorithm=hashes.SHA256(),
		label=None
		)
	)
	return cifrado

def descifrarAESRSA(rutaLlavePrivada, claveCifrada):
	with open(rutaLlavePrivada, "rb") as f:
		llavePrivadaDatos = base64.b64decode(f.read())

	llavePrivada = serialization.load_pem_private_key(
		llavePrivadaDatos,
		password=None
	)

	clave = llavePrivada.decrypt(
		claveCifrada,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return clave
