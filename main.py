import utils.bashToy as bT
import utils.ecdsa as ecdsa

#Para hashear mensaje
#digesto = bT.hashToy(cadena)

P = [476675671136392426, 5963031211007724569, 1]
a = 1
p = 18446744073709551629

#ecdsa.generarClaveECDSA(P, a, p)
#ecdsa.firmarMensaje("Hola mundo", P, a, p)
print(ecdsa.verificar("Hola mundo", P, a, p))


