lista = [(0,1),(1,0),(1,1),(0,0)]
slownik = {(0,0):[(2,1),(2,3)],(0,1):[(2,2),(2,4)]}
lista.remove((0,1))
slownik.pop((0,0))
print(lista)
print(slownik)
