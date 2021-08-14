# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 21:42:25 2020

@author: azul
"""


import imageio
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np
from matplotlib.colors import LogNorm

imagen = plt.imread('archivo')
matriz = imagen[0:3939, 0:3015, 1] 
plt.figure()
plt.imshow(matriz)
plt.colorbar()
#%% 
#las lineas de fondo tiene frecuencia mayor a la del patrón de difracción, entonces me quieor quedar con las más bajas
#calculo la transformada de fourier de las frecuencias que hay en la foto 
imagenfft = np.fft.fft2(matriz, matriz.shape)
imagenfftshifted = np.fft.fftshift(imagenfft) #desplazo el componente de frecuencia cero al centro de la matriz

imagenfftshiftedabs = np.abs(imagenfftshifted) #tomo módulo ya que la transformada es compleja

plt.figure()
plt.imshow(imagenfftshiftedabs, norm=LogNorm()) #ese parámetro es para ver la escala logarítmica en lugar de aplicar el logaritmo a la matriz
plt.colorbar()
#%%
#en este caso quiero las frecuencias bajas que son las de la luz
ventanahorizontal = 18
ventanavertical = 230

#me creo una matriz que coincida con la matriz transformada sólo en un área centrada en las frecuencias bajas, y en el resto sea cero.
imagenfft2recortada = np.zeros((3939, 3015), dtype=complex)#matriz de ceros
imagenfft2recortada[1969-ventanahorizontal:1969+ventanahorizontal, 1507-ventanavertical:1507+ventanavertical] = imagenfftshifted[1969-ventanahorizontal:1969+ventanahorizontal, 1507-ventanavertical:1507+ventanavertical]

plt.figure()
plt.imshow(np.abs(imagenfft2recortada), norm=LogNorm())
plt.colorbar()

#%%

#ahora antitransformo la matriz anterior
imagenfft3 = np.fft.fftshift(imagenfft2recortada) #primero la centro

imagenrecuperada = np.fft.ifft2(imagenfft3, imagenfft3.shape)
imagenrecuperadaabs = np.abs(imagenrecuperada)

plt.figure()
plt.imshow(imagenrecuperadaabs)
plt.colorbar()