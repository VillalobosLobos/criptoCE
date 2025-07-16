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

def descifrarClaveAES(rutaClave, rutaRSA):
	nombreArchivo = os.path.basename(rutaClave)
	nombre = os.path.splitext(nombreArchivo)[0]

	claveCifrada = b64.leerBase64(rutaClave)
	claveDescifrada = rsa.descifrarAESRSA(rutaRSA, claveCifrada)
	b64.guardarBase64(f'data/claves/{nombre}-Descifrada.b64', claveDescifrada)
	print(f"🔑 Clave AES descifrada correctamente en: data/claves/{nombre}-Descifrada.b64")

def descifrarDoc(rutaDoc, rutaClave, rutaNone):
	nombreArchivo = os.path.basename(rutaDoc)
	nombre, extension = os.path.splitext(nombreArchivo)

	rutaDoc = b64.leerBase64(rutaDoc)
	rutaClave = b64.leerBase64(rutaClave)
	rutaNone = b64.leerBase64(rutaNone)

	gcm.descifrarAESGCM(rutaDoc, rutaClave, rutaNone, f'data/documentos/{nombre}-Descifrado.txt')
	print(f'✅ Documento descifrado correctamente en : data/documentos/{nombre}-Descifrado.txt')

def verificarFirma(archivo, rutaFirma):
	with open(archivo, 'r', encoding = 'utf-8') as f:
		mensaje = f.read()
	salida = ecdsa.verificar(mensaje, P, a, p, rutaFirma)
	print(f'{salida}')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Herramienta del empleado")
	subparser = parser.add_subparsers(dest="accion", required=True)

	#Subcomando: Para descifrar la clave AES con su clave privada RSA
	parserClaveAES = subparser.add_parser('descifrar-clave', help='Obtiene la clave AES original')
	parserClaveAES.add_argument('--archivo', required=True, help="Clave cifrada con RSA")
	parserClaveAES.add_argument('--pubkey', required=True, help="Llave privada del empleado")

	#Subcomando: Para descifrar documento
	parserDoc = subparser.add_parser('descifrar-doc', help='Descifra el documento cifrado en AES')
	parserDoc.add_argument('--archivo', required=True, help="Ruta del archivo a descifrar")
	parserDoc.add_argument('--clave', required=True, help="Ruta de la clave para descifrar")
	parserDoc.add_argument('--none', required=True, help="Ruta del none para descifrar")

	#Subcomando: Para verificar la firma
	parserVerificar = subparser.add_parser('verificar', help='Verificar un documento')
	parserVerificar.add_argument('--archivo', required=True, help="Ruta del archivo")
	parserVerificar.add_argument('--firma', required=True, help="Ruta de la firma")

	args = parser.parse_args()

	if args.accion == 'descifrar-clave':
		descifrarClaveAES(args.archivo, args.pubkey)
	elif args.accion == 'descifrar-doc':
		descifrarDoc(args.archivo, args.clave, args.none)
	elif args.accion == 'verificar':
		verificarFirma(args.archivo, args.firma)


