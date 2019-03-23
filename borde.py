from math import fabs

def bordes(imagen, matrizX, matrizY):

	for i in range(len(imagen)):
		for j in range(len(imagen)):
			if ((fabs(matrizY[i][j]) + fabs(matrizY[i][j])) > 7500):
				imagen[i,j]=0

	return imagen
