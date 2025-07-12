import utils.bashToy as bT
import utils.ecdsa as ecdsa

#Para hashear mensaje
#digesto = bT.hashToy(cadena)

P= [1,1,1]
Q= [6,3,1]
G= [476675671136392426, 5963031211007724569, 1]
a= 1
p= 18446744073709551629

#print(ecdsa.sumaPuntos(P, Q, a, p))

print(ecdsa.multiplicarPuntos(1, G, a, p))
print(ecdsa.multiplicarPuntos(2, G, a, p))
print(ecdsa.multiplicarPuntos(3, G, a, p))




