#librerias
from matplotlib import pyplot as plt
import numpy as np
import pydicom
import os
import FileDialog
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PIL
from PIL import ImageTk, Image
import Tkinter as tk
from Tkinter import Label
from tkFileDialog import askopenfilename
from math import fabs

#clases
import kernel
import Gaussian
import mediana
import borde
#variables globales
imgDicom1 = None
ds1 = None
pixArray1 = None
Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]
Gy = [[-1,-2,-1],[0,0,0],[1,2,1]]


def archivo():
	global imgDicom1, ds1, pixArray1

	imgDicom1 = askopenfilename()
	ds1= pydicom.dcmread(imgDicom1)
	pixArray1 = ds1.pixel_array

	for widget in ventanaImagen.winfo_children():
		widget.destroy()

	figure = plt.Figure()
	subPlot = figure.add_subplot(111)
	subPlot.imshow(pixArray1, cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(figure, master=ventanaImagen)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack(padx=5, pady=15)

	mostrarInfo()

def filtroGau():
	kernel1, escalar = Gaussian.get_gaussian_filter()
	nuevaMatriz = kernel.aplicarKernel(pixArray1,kernel1,escalar)

	for widget in ventanaFiltro.winfo_children():
		widget.destroy()

	figure = plt.Figure()
	subPlot = figure.add_subplot(111)
	subPlot.imshow(nuevaMatriz, cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(figure, master=ventanaFiltro)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack(padx=5, pady=15)

def rayleigh():
	kernel1, escalar = Gaussian.get_rayleigh_filter()
	nuevaMatriz = kernel.aplicarKernel(pixArray1, kernel1,escalar)

	for widget in ventanaFiltro.winfo_children():
		widget.destroy()

	figure = plt.Figure()
	subPlot = figure.add_subplot(111)
	subPlot.imshow(nuevaMatriz, cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(figure, master=ventanaFiltro)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack(padx=5, pady=15)

def sobel():
	imagenCopia = pixArray1.copy()
	gradienteX = kernel.aplicarKernel(pixArray1, Gx,1)
	gradienteY = kernel.aplicarKernel(pixArray1, Gy,1)

	imagenCopia = borde.bordes(imagenCopia, gradienteX, gradienteY)

	for widget in ventanaFiltro.winfo_children():
		widget.destroy()

	figure = plt.Figure()
	subPlot = figure.add_subplot(111)
	subPlot.imshow(imagenCopia, cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(figure, master=ventanaFiltro)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack(padx=5, pady=15)

def archivohistograma():

	rows = int(ds1.Rows)
	columns = int(ds1.Columns)
	intensity = [0]*65536

	for i in range(rows):
		for j in range(columns):
			intensity[ds1.pixel_array[i,j]] = intensity[ds1.pixel_array[i,j]]+1
	
	intensity = np.asarray(intensity)
	plt.plot(intensity)
	plt.show()

def filtroMediana():
	rows = int(ds1.Rows)
	columns = int(ds1.Columns)
	nuevaMatriz = mediana.filtroMed(pixArray1, 1, rows, columns)

	for widget in ventanaFiltro.winfo_children():
		widget.destroy()

	figure = plt.Figure()
	subPlot = figure.add_subplot(111)
	subPlot.imshow(nuevaMatriz, cmap=plt.cm.gray)
	imagesTemp = FigureCanvasTkAgg(figure, master=ventanaFiltro)
	imagesTemp.draw()
	imagesTemp.get_tk_widget().pack(padx=5, pady=15)


def infoImagen (imagen):
	info = ""

	try:
		info += "Patient ID:" + str(imagen.PatientID) + "\n\n" 
	except AttributeError:
			info += "Patient ID: no disponible" + "\n\n"
	try:
		info += "Sequence Name:" + str(imagen.SequenceName) + "\n\n" 
	except AttributeError:
			info += "Sequence Name: no disponible" + "\n\n"		
	try:
		info += "Strain Description:" + str(imagen.StrainDescription) + "\n\n" 
	except AttributeError:
			info += "Strain Description: no disponible" + "\n\n"		
	try:
		info += "Largest Image Pixel Value:" + str(imagen.LargestImagePixelValue) + "\n\n" 
	except AttributeError:
			info += "Largest Image Pixel Value: no disponible" + "\n\n"
	try:
		info += "Smallest Image Pixel Value:" + str(imagen.SmallestImagePixelValue) + "\n\n"
	except AttributeError:
		info += "Smallest Image Pixel Value: no disponible" + "\n\n"
	try:
		info += "Columns:" + str(imagen.Columns) + "\n\n"
	except AttributeError:
		info += "Columns: no disponible" + "\n\n"
	try:
		info += "Rows:" + str(imagen.Rows) + "\n\n"
	except AttributeError:
		info += "Rows: no disponible" + "\n\n"
	try:
		info += "Pixel Spacing:" + str(imagen.PixelSpacing) + "\n\n"
	except AttributeError:
		info += "Pixel Spacing: no disponible" + "\n\n"
	try:
		info += "MR Acquisition Type:" + str(imagen.MRAcquisitionType) + "\n\n"
	except AttributeError:
		info += "MR Acquisition Type: no disponible" + "\n\n"

	return info

def mostrarInfo():
	labelInfo['text'] = infoImagen(ds1)


#intentos

PathDicom = "./dicom/MRI/"
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))

#obtenemos la imagen dicom para mostrar en la ventana
#plt.imshow(np.flipud(pixArray),cmap=plt.cm.gray)
#plt.show()

#interfaz grafica
ventana = tk.Tk()

#titulo de la ventana
ventana.title('Dicom')

#medidas de la ventana, cuestiones de tamano y fondo
ventana.resizable(width=TRUE, height=TRUE)
ventana.configure(background = 'dark slate gray')
ventana.geometry("1000x1000")


#boton para seleccionar imagen
boton = Button(ventana, text="Seleccionar imagen", command=archivo)
boton.pack(padx=5, pady=5,side = tk.TOP)

#boton para mostrar histograma
botonHis = Button(ventana, text = "Histograma", command=archivohistograma)
botonHis.pack(padx=5, pady=5, side = tk.RIGHT)
botonHis.place(x = 200, y =70)

#boton para filtro gaussiano
botonGau = Button(ventana, text = "Filtro gaussiano", command = filtroGau)
botonGau.pack(padx=5, pady=5)
botonGau.place(x = 60, y =70)

#boton para rayleight
botonGau = Button(ventana, text = "Rayleigh", command = rayleigh)
botonGau.pack(padx=5, pady=5)
botonGau.place(x = 310, y =70)

#boton para mediana
botonMed =  Button(ventana, text = "Mediana", command = filtroMediana)
botonMed.pack(padx=5, pady=5)
botonMed.place(x = 400, y =70)

#boton sobel
botonSobel = Button(ventana, text = "Sobel", command = sobel)
botonSobel.pack(padx=5, pady=5)
botonSobel.place(x=500, y=70)

#sub-ventana imagen
ventanaImagen=tk.Frame(ventana, bg="dark slate gray")
ventanaImagen.pack(side = tk.RIGHT)

#mostrar informacion imagen
ventanaInfo=tk.Frame(ventana, bg="dark slate gray")
ventanaInfo.pack(side = tk.LEFT, padx = 8, pady = 8)

#mostrar imagen con filtros
ventanaFiltro = tk.Frame(ventana, bg = "dark slate gray")
ventanaFiltro.pack(side = tk.RIGHT, padx = 8, pady = 8)

labelInfo = tk.Label(ventanaInfo, text = "", bg = "dark slate gray", fg = "white", height=30, width=35)
labelInfo.pack()

#ejecucion de la ventana
ventana.mainloop()