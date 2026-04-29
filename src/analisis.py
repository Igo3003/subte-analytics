import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from matplotlib.colors import PowerNorm
from lectura_de_archivos import a,b,c,d,e,h,lista_lineas,Linea
from pathlib import Path
import ast

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"




def convertir_a_horario(x: float):
    h = int(x)
    m = int((x - h) * 60)
    return f"{h:02d}:{m:02d}"

def dividir_lista(l, e):
    return [x / e for x in l]

def leer_info(lista_lineas: list[Linea]):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "info.txt",'r') as file:
        info = file.read()
    
    lineas = info.strip().split("\n")
    desde = 0
    for l in range(len(lista_lineas)):
        linea = lista_lineas[l]
        linea.viajes_totales = int(lineas[l+2].split(":")[1].strip())
        linea.promedio_hora = dividir_lista(ast.literal_eval(lineas[3].split(":", 1)[1].strip()),366)#Cambiar a 365 si el año no es biciesto

        linea.diccionario_estaciones = ast.literal_eval(lineas[4].split(":", 1)[1].strip())

# Datos precalculados a partir de lectura_de_archivos.py
# para evitar reprocesar CSVs pesados
def armar_graficos():
    leer_info(lista_lineas)


    lineas = [l.nombre[-1] for l in lista_lineas]
    colores = ["tab:cyan","tab:red","tab:blue", "tab:green","darkviolet","gold"]
    
    # -------------------- Gráfico de uso de líneas -------------------
    fig, ax = plt.subplots()
    
    ax.bar(lineas,[l.viajes_totales for l in lista_lineas],color=colores)
    ax.set_title("Viajes totales por línea de Subte")
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "viajes_por_linea.png")
    

    # -------------------- Gráfico de uso de líneas por estación ------
    v_t = [(l.viajes_totales//l.longitud) for l in lista_lineas]
    fig, ax = plt.subplots()
    
    ax.bar(lineas,v_t,color=colores)
    ax.set_title("Viajes totales por Estación")
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "viajes_por_linea_y_estacion.png")
    
    
    # -------------------- Gráfico de uso de cada linea -------------------
    for i in range(len(lineas)):
        fig, ax = plt.subplots(figsize=(14,5))

        ax.bar(lista_lineas[i].diccionario_estaciones.keys(), lista_lineas[i].diccionario_estaciones.values(),color=colores[i])
        ax.set_title("Viajes por estación - Línea " + lineas[i])
        ax.tick_params(axis='x', rotation=45)
        
        OUTPUT_DIR.mkdir(exist_ok=True)
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / f"viajes_por_estacion_{lineas[i]}.png")
    

        # -------------------- heatmap Horas pico -------------------
    horario = [convertir_a_horario(5.25 +i/4)if i%4 == 3  else "" for i in range(73)]#Empiezan a las 5:15 y son 73 cuartos de hora hasta el cierre de la última
    data_array = [dividir_lista(l.promedio_hora,l.viajes_dia_promedio) for l in lista_lineas]
    fig, ax = plt.subplots()
    im = ax.imshow(data_array,cmap="viridis",aspect='auto',norm=PowerNorm(gamma=0.8))

    ax.set_xticks(range(len(horario)), labels=horario, rotation=90)
    ax.set_yticks(range(len(lineas)), labels=lineas)



    ax.set_title("Uso relativo por línea y horario")
    ax.set_xlabel("Hora")
    ax.set_ylabel("Línea")
    fig.colorbar(im,ax=ax)
    fig.tight_layout()



    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.savefig(OUTPUT_DIR / "Uso_relativo.png")

