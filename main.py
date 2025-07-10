import utils.bashToy as bT

print("Ingrese cadena: ",end='')
cadena = input()

digesto = bT.hashToy(cadena)
print(digesto)

