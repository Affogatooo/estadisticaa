import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Declaración de funciones para calcular las medidas de tendencia central de una lista de números.
def desviacionestandar(datos):
    media = sum(datos)/len(datos)
    sumatoria = 0
    for i in datos:
        sumatoria += (i - media)**2
    return round((sumatoria/len(datos))**0.5,2)

def varianza(datos):
    media = sum(datos)/len(datos)
    sumatoria = 0
    for i in datos:
        sumatoria += (i - media)**2
    return round(sumatoria/len(datos),2)

def moda(datos):
    repeticiones = 0
    for i in datos:
        n = datos.count(i)
        if n > repeticiones:
            repeticiones = n
    moda = []
    for i in datos:
        n = datos.count(i)
        if n == repeticiones and i not in moda:
            moda.append(i)
    return moda

def mediana(datos):
    datos.sort()
    if len(datos) % 2 == 0:
        n = len(datos)
        mediana = (datos[int(n/2)-1] + datos[int(n/2)])/2
    else:
        mediana = datos[int(len(datos)/2)]
    return mediana

def media(datos):
    return sum(datos)/len(datos)


# Declaración de funciones para poder realizar una representación tabular de frecuencias de una lista de números.
def clases(datos):
    return math.ceil(1 + (3.322*math.log10(len(datos))))

def rango(datos):
    return max(datos) - min(datos)

def amplitud(datos):
    return round(rango(datos)/clases(datos),2)

def intervalosdeclase(datos):
    intervalosdeclase = []
    for i in range(clases(datos)):
        if i == 0:
            intervalosdeclase.append([min(datos), min(datos) + amplitud(datos)])
        else:
            intervalosdeclase.append([intervalosdeclase[-1][1], intervalosdeclase[-1][1] + amplitud(datos)])
    return intervalosdeclase

def frecuenciaabsoluta(datos):
    frecuenciaabsoluta = []
    for i in intervalosdeclase(datos):
        n = 0
        for j in datos:
            if j >= i[0] and j < i[1]:
                n += 1
        frecuenciaabsoluta.append([i, n])
    return frecuenciaabsoluta

def frecuenciaabsolutaacumulada(datos):
    frecuenciaabsolutaacumulada = []
    for i in frecuenciaabsoluta(datos):
        if len(frecuenciaabsolutaacumulada) == 0:
            frecuenciaabsolutaacumulada.append(i)
        else:
            frecuenciaabsolutaacumulada.append([i[0], i[1] + frecuenciaabsolutaacumulada[-1][1]])
    return frecuenciaabsolutaacumulada

def frecuenciarelativa(datos):
    frecuenciarelativa = []
    for i in frecuenciaabsoluta(datos):
        frecuenciarelativa.append([i[0], i[1]/len(datos)])
    return frecuenciarelativa

def frecuenciarelativaacumulada(datos):
    frecuenciarelativaacumulada = []
    for i in frecuenciarelativa(datos):
        if len(frecuenciarelativaacumulada) == 0:
            frecuenciarelativaacumulada.append(i)
        else:
            frecuenciarelativaacumulada.append([i[0], round(i[1] + frecuenciarelativaacumulada[-1][1],2)])
    return frecuenciarelativaacumulada

def primervalordelarray(array):
    valores = []
    for i in array:
        valores.append(i[0])
    return valores

def segundovalordelarray(array):
    valores = []
    for i in array:
        valores.append(i[1])
    return valores

# Inicio del programa.

# Obtiene los datos y los pone dentro de un array de números.
numbers = input("Lista de numeros separados por comas: ")
numbers = numbers.split(",")
numbers = [int(i) for i in numbers]

devstd = desviacionestandar(numbers)
varianza = varianza(numbers)
media = media(numbers)
mediana = mediana(numbers)
moda = moda(numbers)

print("Varianza: " + str(varianza))
print("Desviación estándar: " + str(devstd))
print("Media: " + str(media))
print("Mediana: " + str(mediana))
print("Moda: " + str(moda))

print("Clases: " + str(clases(numbers)))
print("Rango: " + str(rango(numbers)))
print("Amplitud: " + str(amplitud(numbers)))
# print("Frecuencia absoluta: " + str(segundovalordelarray(frecuenciaabsoluta(numbers))))
# print("Frecuencia absoluta acumulada: " + str(segundovalordelarray(frecuenciaabsolutaacumulada(numbers))))
# print("Frecuencia relativa: " + str(segundovalordelarray(frecuenciarelativa(numbers))))
# print("Frecuencia relativa acumulada: " + str(segundovalordelarray(frecuenciarelativaacumulada(numbers))))
print("Frecuencia absoluta: " + str(frecuenciaabsoluta(numbers)))
print("Frecuencia absoluta acumulada: " + str(frecuenciaabsolutaacumulada(numbers)))
print("Frecuencia relativa: " + str(frecuenciarelativa(numbers)))
print("Frecuencia relativa acumulada: " + str(frecuenciarelativaacumulada(numbers)))
print("Intervalos: " + str(intervalosdeclase(numbers)))

pp = PdfPages('tabladefrecuencias.pdf')
df = pd.DataFrame()

# columnas
df['Intervalos'] = primervalordelarray(frecuenciaabsoluta(numbers))
df['Frecuencia absoluta'] = segundovalordelarray(frecuenciaabsoluta(numbers))
df['Frecuencia absoluta acumulada'] = segundovalordelarray(frecuenciaabsolutaacumulada(numbers))
df['Frecuencia relativa'] = segundovalordelarray(frecuenciarelativa(numbers))
df['Frecuencia relativa acumulada'] = segundovalordelarray(frecuenciarelativaacumulada(numbers))

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, loc='center')

fig.tight_layout()

# add central tendency measures to the page below the table
ax.text(0.18, 0.1, "Varianza: " + str(varianza) + "\nDesviación estándar: " + str(devstd) + "\nMedia: " + str(media) + "\nMediana: " + str(mediana) + "\nModa: " + str(moda), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
ax.texts[0].set_fontsize(6)

pp.savefig(fig)
pp.close()