import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

class Linea():
    def __init__(self,nombre, diccionario_estaciones :dict):
        self.nombre = nombre
        self.viajes_totales = 0
        self.viajes_dia_promedio = 0
        self.promedio_hora = [0]*73 #de 5:15 a 23:30
        self.longitud = len(diccionario_estaciones.keys())
        self.diccionario_estaciones = diccionario_estaciones


def reconocer_horario(horario: str)->int: #devuelve el número que sería en la lista de horarios
    hora = int(horario[0:2])
    min = int(horario[3:5])
    return int(hora*4+min/15-21)

def encontrar(l,e):
    i = 0
    while i<len(l):
        if l[i]==e: return i
        i+=1
    return -1

def reconocer_linea(lista_lineas, fila: str)->Linea:
    return lista_lineas[encontrar(["A","B","C","D","E","H"],fila["LINEA"][-1])]

def sumar_en_estacion(linea: Linea, estacion: str, cantidad: int):
    if estacion in linea.diccionario_estaciones.keys():
        linea.diccionario_estaciones[estacion]+=cantidad

def sumar_en_horario(linea: Linea, horario: int, cantidad: int):
    linea.promedio_hora[horario]+=cantidad

def sumar(linea: Linea, estacion: str, horario: int, cantidad: int):
    linea.viajes_totales+=1
    sumar_en_estacion(linea,estacion,cantidad)
    sumar_en_horario(linea,horario,cantidad)

def leer_archivo(nombre_archivo:str):
    df = pd.read_csv(DATA_DIR / nombre_archivo,sep=";", encoding="latin1")
    for i in range(len(df)-1):
        fila = df.iloc[i]
        horario = reconocer_horario(fila["DESDE"])
        cantidad = int(fila["pax_TOTAL"])
        estacion = fila["ESTACION"]
        if horario<73:
            linea : Linea = reconocer_linea(lista_lineas,fila)
            sumar(linea,estacion,horario,cantidad)

def leer_todos_los_archivos(lista_archivos):
    for nombre_archivo in lista_archivos:
        leer_archivo(nombre_archivo)

def imprimir_data(lista_lineas: list[Linea]):
    with open(BASE_DIR / "outputs" / "info.txt","w") as archivo:
        res=""
        for linea in lista_lineas:
            res += f"{linea.nombre}\n\nviajes totales: {linea.viajes_totales}\nlista de horarios: {linea.promedio_hora}\ndiccionario de estaciones: {linea.diccionario_estaciones}\n\n\n"
        archivo.write(res)



estaciones_a = {
    "San Pedrito": 0,
    "Flores": 0,
    "Carabobo": 0,
    "Puan": 0,
    "Primera Junta": 0,
    "Acoyte": 0,
    "Rio de Janeiro": 0,
    "Castro Barros": 0,
    "Loria": 0,
    "Plaza Miserere": 0,
    "Alberti": 0,
    "Pasco": 0,
    "Congreso": 0,
    "Saenz Peña ": 0,
    "Lima": 0,
    "Piedras": 0,
    "Peru": 0,
    "Plaza de Mayo": 0
}
estaciones_b = {
    "Rosas": 0,
    "Echeverria": 0,
    "Los Incas": 0,
    "Tronador": 0,
    "Federico Lacroze": 0,
    "Dorrego": 0,
    "Malabia": 0,
    "Angel Gallardo": 0,
    "Medrano": 0,
    "Carlos Gardel": 0,
    "Pueyrredon": 0,
    "Pasteur": 0,
    "Callao.B": 0,
    "Uruguay": 0,
    "Carlos Pellegrini": 0,
    "Florida": 0,
    "Leandro N. Alem" :0
}
estaciones_c =  {
    "Constitucion":0,
    "San Juan":0,
    "Independencia":0,
    "Mariano Moreno":0,
    "Avenida de Mayo":0,
    "Diagonal Norte":0,
    "Lavalle":0,
    "General San Martin":0,
    "Retiro":0
}
estaciones_d =  {
    "Congreso de Tucuman":0,
    "Juramento":0,
    "Jose Hernandez":0,
    "Olleros":0,
    "Ministro Carranza":0,
    "Palermo":0,
    "Plaza Italia":0,
    "Scalabrini Ortiz":0,
    "Bulnes":0,
    "Agüero":0,
    "Pueyrredon.D":0,
    "Facultad de Medicina":0,
    "Callao":0,
    "Tribunales":0,
    "9 de julio":0,
    "Catedral":0
}
estaciones_e = {
    "Pza. de los Virreyes":0,
    "Varela":0,
    "Medalla Milagrosa":0,
    "Emilio Mitre":0,
    "Jose Maria Moreno":0,
    "Avenida La Plata":0,
    "Boedo":0,
    "Urquiza":0,
    "Jujuy":0,
    "Pichincha":0,
    "Entre Rios":0,
    "San Jose":0,
    "Independencia.H":0,
    "General Belgrano":0,
    "Bolivar":0,
    "Correo Central":0,
    "Catalinas":0,
    "Retiro E":0,
}
estaciones_h = {
    "Hospitales":0,
    "Patricios":0,
    "Caseros":0,
    "Inclan":0,
    "Humberto I":0,
    "Venezuela":0,
    "Once":0,
    "Corrientes":0,
    "Cordoba":0,
    "Santa Fe":0,
    "Las Heras":0,
    "Facultad de Derecho":0
}




a = Linea("LineaA",estaciones_a)
b = Linea("LineaB",estaciones_b)
c = Linea("LineaC",estaciones_c)
d = Linea("LineaD",estaciones_d)
e = Linea("LineaE",estaciones_e)
h = Linea("LineaH",estaciones_h)

lista_lineas = [a,b,c,d,e,h]
lista_archivos = ["202401_PAX15min-ABC.csv","202401_PAX15min-DEH.csv",
                "202402_PAX15min-ABC.csv","202402_PAX15min-DEH.csv",
                "202403_PAX15min-ABC.csv","202403_PAX15min-DEH.csv",
                "202404_PAX15min-ABC.csv","202404_PAX15min-DEH.csv",
                "202405_PAX15min-ABC.csv","202405_PAX15min-DEH.csv",
                "202406_PAX15min-ABC.csv","202406_PAX15min-DEH.csv",
                "202407_PAX15min-ABC.csv","202407_PAX15min-DEH.csv",
                "202408_PAX15min-ABC.csv","202408_PAX15min-DEH.csv",
                "202409_PAX15min-ABC.csv","202409_PAX15min-DEH.csv",
                "202410_PAX15min-ABC.csv","202410_PAX15min-DEH.csv",
                "202411_PAX15min-ABC.csv","202411_PAX15min-DEH.csv",
                "202412_PAX15min-ABC-INCLUYEOTROMODOSDEPAGO.csv","202412_PAX15min-DEH-INCLUYEOTROMODOSDEPAGO.csv"]


if __name__ == "__main__":
    leer_todos_los_archivos(lista_archivos)
    imprimir_data(lista_lineas)