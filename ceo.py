#Para hacer una interfaz de linea de comando 'CLI'
import utils.ecdsa as ecdsa
import utils.rsaOAEP as rsa
import utils.aesGCM as gcm
import utils.base64 as b64
import argparse
import os

P = [476675671136392426, 5963031211007724569, 1]
a = 1
p = 18446744073709551629

def generarClavePublicaPrivadaEmpleado(nombre):
	rsa.generarClavesRSA(nombre)

def generarClavePublicaPrivada():
	ecdsa.generarClaveECDSA(P, a, p)

def firmar(archivo):
	with open(archivo, 'r', encoding = 'utf-8') as f:
		mensaje = f.read()
	ecdsa.firmarMensaje(mensaje, P, a, p, archivo)
	print(f"✅ Documento firmado correctamente: {archivo}")

def cifrarDocumento(archivo):
	cifrado, clave, nonce = gcm.cifrarAESGCM(archivo)
	nombreArchivo = os.path.basename(archivo)
	nombre = os.path.splitext(nombreArchivo)[0]

	#Guardaremos en base 64 el cifrado, clave y el nonce
	b64.guardarBase64(f'data/documentos/{nombre}-Cifrado.b64', cifrado)
	b64.guardarBase64(f'data/claves/{nombre}-ClaveAES.b64', clave)
	b64.guardarBase64(f'data/claves/{nombre}-Nonce.b64', nonce)

	print(f"🔐 Documento cifrado correctamente con AES-GCM.")
	print(f"🔑 Clave AES guardada en: data/claves/{nombre}-ClaveAES.b64")
	print(f"🧂 Nonce guardado en: data/claves/{nombre}-Nonce.b64")
	print(f"📄 Cifrado guardado en: data/documentos/{nombre}-Cifrado.b64")

def cifrarClaveAES(rutaAES, rutaRSA):
	nombreAES = os.path.basename(rutaAES)
	nombre = os.path.splitext(nombreAES)[0]

	claveAES = b64.leerBase64(rutaAES)
	cifradaRSA = rsa.cifrarAESRSA(rutaRSA, claveAES)
	b64.guardarBase64(f"data/claves/{nombre}-Cifrada.b64", cifradaRSA)
	print(f"🔐 Clave AES cifrada usando RSA guardada en : data/claves/{nombre}-Cifrada.b64")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Herramienta del CEO")
	subparser = parser.add_subparsers(dest="accion", required=True)

	#Subcomando: Para generar clave pública y privada
	parserGenerarLlaves = subparser.add_parser('generar-claves-ecdsa', help='Generar llaves con ECDSA')

	#Subcomando: Para generar clave RSA para un empleado
	parserGenerarLlavesEmpleado = subparser.add_parser('generar-claves-rsa', help='Generar llaves con ECDSA')
	parserGenerarLlavesEmpleado.add_argument('--nombre', required=True, help="Nombre del empleado")

	#Subcomando: firmar
	parser_firmar = subparser.add_parser('firmar', help='Firmar un archivo con ECDSA')
	parser_firmar.add_argument('--archivo', required=True, help="Ruta del archivo a firmar")

	#Subcomando: cifrar documento
	parser_cifrar = subparser.add_parser('cifrar-doc', help='Cifrar documento con AES-GCM')
	parser_cifrar.add_argument('--archivo', required=True, help="Ruta del archivo a cifrar")

	#Subcomando: cifrar clave AES con RSA
	parserCifrarClave = subparser.add_parser('cifrar-clave', help='Cifrar una clave AES con la clave pública de un empleado (RSA-OAEP)')
	parserCifrarClave.add_argument('--aes', required=True, help='Ruta a la clave AES en base64')
	parserCifrarClave.add_argument('--pubkey', required=True, help='Ruta a la clave pública del empleado (base64)')

	args = parser.parse_args()

	if args.accion == 'firmar':
		firmar(args.archivo)
	elif args.accion == 'cifrar-doc':
		cifrarDocumento(args.archivo)
	elif args.accion == 'cifrar-clave':
		cifrarClaveAES(args.aes, args.pubkey)
	elif args.accion == 'generar-claves-ecdsa':
		generarClavePublicaPrivada()
	elif args.accion == 'generar-claves-rsa':
		generarClavePublicaPrivadaEmpleado(args.nombre)





