import base64

def guardarBase64(ruta, datosBytes):
	with open(ruta, 'wb') as f:
		f.write(base64.b64encode(datosBytes))

def leerBase64(ruta):
	with open(ruta, 'rb') as f:
		return base64.b64decode(f.read())


