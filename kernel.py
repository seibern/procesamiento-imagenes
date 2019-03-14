

def nuevaPos(matriz, matrizKernel, i, j, factorValue):
	kernel = (len(matrizKernel) - 1)/2
	contador1 = 0
	contador2 = 0
	vlrKernel = 0

	for a in range(i - kernel,i + kernel):
		for b in range(j - kernel,j + kernel):
			vlrKernel = vlrKernel + (matriz[a][b] * matrizKernel[contador1][contador2])
			contador2 = contador2 +1

		contador1 = contador1 +1
		contador2 = 0

	return vlrKernel / factorValue


def aplicarKernel(matriz, matrizKernel, factorValue):
	kernel = (len(matrizKernel) - 1)/2
	nuevaMatriz = [0]*len(matriz)

	for i in range(0, len(matriz)):
		nuevaMatriz[i] = [0]*len(matriz)

		for j in range(0, len(matriz)):
			if((i < kernel) or (j < kernel) or (i > len(matriz) - kernel) or (j > len(matriz) - kernel)):
				nuevaMatriz[i][j] = matriz[i][j]
			else:
				nuevaMatriz[i][j] = nuevaPos(matriz, matrizKernel, i, j, factorValue)

	return nuevaMatriz

