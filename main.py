import utils.bashToy as bT
import utils.ecdsa as ecdsa

#Para hashear mensaje
#digesto = bT.hashToy(cadena)

P = [476675671136392426, 5963031211007724569, 1]
a = 1
p = 18446744073709551629

#print(f'doblado de puntos : {ecdsa.dobladoPuntos(P, P, a, p)}')

for i in [1, 2, 3, 4, 5]:
	print(f'{i}P = {ecdsa.multiplicarPuntos(i, P, a, p)}')

for i in [100, 500, 1000, 5000, 10000]:
	print(f'{i}P = {ecdsa.multiplicarPuntos(i, P, a, p)}')






