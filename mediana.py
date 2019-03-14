def ordenar (lista):
	largo = len(lista)

	for i in range(0, largo):
		for j in range (0, largo-i-1):
			if lista[j] > lista[j+1]:
				lista[j], lista [j+1] = lista[j+1],lista[j]

	return lista


def filtroMed (imagen, numeroVecinos, rows, columns):
	for i in range(rows):
		for j in xrange(columns):
			
			if i == 0 or i == rows-1 or j == 0 or j == columns-1:
				imagen[i,j] = 0

			else:
				list = []
				
				for x in range(int(i-numeroVecinos), int(i+numeroVecinos)):
					for y in range(int(j-numeroVecinos), int(i+numeroVecinos)):
							list.append(imagen[x,y])

	return imagen