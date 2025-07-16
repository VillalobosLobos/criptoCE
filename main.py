import utils.ecdsa as ecdsa
import utils.rsaOAEP as rsa
import utils.aesGCM as gcm
import utils.bashToy as bT
import utils.base64 as b64

#Para hashear mensaje
#digesto = bT.hashToy(cadena)

P = [476675671136392426, 5963031211007724569, 1]
a = 1
p = 18446744073709551629

#ecdsa.generarClaveECDSA(P, a, p)
#ecdsa.firmarMensaje("Hola mundo", P, a, p)
#print(ecdsa.verificar("Hola mundo", P, a, p))

#cifrado, clave, nonce = gcm.cifrarAESGCM('data/documentos/ejemploTxt.txt')

# --- Guardado como base64 ---
#b64.guardarBase64('data/documentos/cifrado.b64', cifrado)
#b64.guardarBase64('data/claves/claveAES.b64', clave)
#b64.guardarBase64('data/claves/nonce.b64', nonce)

# --- Lectura (solo para probar que lo puedes descifrar después) ---
#cifradoLeido = b64.leerBase64('data/documentos/cifrado.b64')
#claveLeida = b64.leerBase64('data/claves/claveAES.b64')
#nonceLeido = b64.leerBase64('data/claves/nonce.b64')

#gcm.descifrarAESGCM(cifradoLeido, claveLeida, nonceLeido, 'data/documentos/ejemploTxtSalida.txt')

# 1. Generar par de claves (solo una vez por usuario)
rsa.generarClavesRSA()

# 2. Leer la clave AES original
clave_aes = b64.leerBase64("data/claves/claveAES.b64")

# 3. Cifrar con clave pública RSA
cifrada_rsa = rsa.cifrarAESRSA("data/claves/rsaPublica.pem", clave_aes)

# 4. Guardar la clave cifrada (por ejemplo, para el empleado)
b64.guardarBase64("data/claves/claveAES_cifrada.b64", cifrada_rsa)

# 5. Luego el empleado la desencripta con su clave privada
cifrada_leida = b64.leerBase64("data/claves/claveAES_cifrada.b64")
clave_descifrada = rsa.descifrarAESRSA("data/claves/rsaPrivada.pem", cifrada_leida)



