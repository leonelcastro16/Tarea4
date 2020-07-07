#!/usr/bin/env python
# coding: utf-8

# # Tarea 4
# ## Leonel Castro Ulloa 
# ## B58219

# In[72]:




import pandas as pd
import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt

data =np.array(pd.read_csv("bits10k.csv",header= None))
# Se define a N los datos del excel 
N = len(data) 
f = 5000   # se define la frecuencia en 5000 Hz 
T = 1/f    # se define el periodo 
p= 50       # Se asignan la cantidad de muestras 
tp = np.linspace(0, T, p)
# forma senoidal de la onda
sen = np.sin(2*np.pi * f * tp)

# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, len(data)*T, len(data)*p)

# Inicializar el vector de la señal modulada Tx
senal = np.zeros(t.shape)
# Creación de la señal modulada BPSK
for i, j in enumerate (data):
    if j==1:
        
        senal[i*p:(i+1)*p]=sen
    
    else:
        senal[i*p:(i+1)*p]= -sen

# Visualización de los primeros bits modulados

plt.plot(senal[0:5*p])
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Señal modulada')


# ## Punto 2
# 

# In[73]:


# Potencia instantánea
Pinst = senal**2

# Potencia promedio a partir de la potencia instantánea (W)
Ps = integrate.trapz(Pinst, t) / (N * T)
print("El valor de la potencia es de: ", Ps)


# ## Punto 3

# In[75]:


# Relación señal-a-ruido deseada
SNR = 0



# Potencia del ruido para SNR y potencia de la señal dadas
Pn = Ps / (10**(SNR / 10))

# Desviación estándar del ruido
sigma = np.sqrt(Pn)

# Crear ruido (Pn = sigma^2)
ruido = np.random.normal(0, sigma, senal.shape)

# Simular "el canal": señal recibida
Rx = senal + ruido

# Visualización de los primeros bits recibidos
pb = 5
plt.figure()
plt.plot(Rx[0:pb*p])
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Canal ruidoso del tipo AWGN')
plt.show()


# ## Punto 4

# In[76]:


# Antes del canal ruidoso
fs=p/T #
fw, PSD = signal.welch(senal, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.title('Antes del canal ruidoso.')
plt.show()

# Después del canal ruidoso
fw, PSD = signal.welch(Rx, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.title('Despúes del canal ruidoso.')
plt.show()


# ## Punto 5

# In[85]:


# asignación del rango de valores de dB 
SNR2=np.arange(-2,4)
BER2= np.zeros(SNR2.shape)
Es = np.sum(sen**2)
for o in range(len(SNR2)):
    pn2=Ps/(10**(SNR2[o]/10))
    res2=np.sqrt(pn2)
    gra=np.random.normal(0,res2,senal.shape)
    Rx2=senal+gra
    dataRx2=np.zeros(data.shape)
    
    for w, z in enumerate(data):
        Ep2 = np.sum(Rx2[w*p:(w+1)*p] * sen)
        if Ep2 > Es/2:
            dataRx2[w] = 1
        else:
            dataRx2[w] = 0

    err2 = np.sum(np.abs(data - dataRx2))
    BER2[o] = err2/N
    print('Hay un total de {} errores, para una tasa de error de {} en el dB {}.'.format(err2, BER2[o], SNR2[o]))


# ## Punto 6 

# In[86]:



plt.figure()
plt.plot(SNR2,BER2) 
plt.xlabel('SNR(dB)')
plt.ylabel('Ber')
plt.title('Ber vs SNR')


# In[ ]:




