import utils.bashToy as bT
import utils.ecdsa as ecdsa

#Para hashear mensaje
#digesto = bT.hashToy(cadena)

P= [5,1,1]
Q= [6,3,1]
a= 2
p= 17

print(ecdsa.sumaPuntos(P, Q, a, p))


