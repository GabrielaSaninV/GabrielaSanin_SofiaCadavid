import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import os
class CalAir:
    def __init__(self, ruta):
        self._ruta = ruta
        # Atributo '_df': DataFrame de pandas que almacenará los datos cargados. Se inicializa como None.
        self._df = None
        # Atributo '_info_columnas': Diccionario para mapear nombres cortos de columnas a nombres completos y unidades para visualización.
        # Esto permite mostrar etiquetas de gráficos y resultados con unidades y nombres amigables (ej: 'Material Particulado 2.5 (µg/m³)').
        self._info_columnas = {
            'pm25': {'nombre_visualizacion': 'Material Particulado 2.5', 'unidad': '(µg/m³)'},
            'pm10': {'nombre_visualizacion': 'Material Particulado 10', 'unidad': '(µg/m³)'},
            'no': {'nombre_visualizacion': 'Monóxido de Nitrógeno', 'unidad': '(µg/m³)'},
            'no2': {'nombre_visualizacion': 'Dióxido de Nitrógeno', 'unidad': '(µg/m³)'},
            'nox': {'nombre_visualizacion': 'Óxidos de Nitrógeno', 'unidad': '(µg/m³)'},
            'ozono': {'nombre_visualizacion': 'Ozono', 'unidad': '(µg/m³)'},
            'co': {'nombre_visualizacion': 'Monóxido de Carbono', 'unidad': '(ppm)'}
        }
    def obtener_nombre_y_unidades_visualizacion(self, nombre_columna):
            # Método que obtiene el nombre completo y las unidades de una columna para su uso en gráficos o salidas.
            # .get() permite obtener el valor de la clave; si la clave no existe, devuelve el segundo argumento (un diccionario por defecto).
            informacion = self._info_columnas.get(nombre_columna, {'nombre_visualizacion': nombre_columna, 'unidad': ''})
            # Retorna la cadena formateada, uniendo el nombre y la unidad. .strip() elimina espacios en blanco al inicio/fin.
            return f"{informacion['nombre_visualizacion']} {informacion['unidad']}".strip()

    def cargar_df(self):
        self._df = pd.read_csv(self._ruta)
        # Se verifica si la columna 'fecha_hora' existe en el DataFrame.
        if 'fecha_hora' in self._df.columns:
            try:
                # pd.to_datetime(): Convierte la columna 'fecha_hora' a tipo datetime. Esto es CRÍTICO para el análisis de series temporales.
                self._df['fecha_hora'] = pd.to_datetime(self._df['fecha_hora'])
                # .set_index(): Establece la columna 'fecha_hora' como el índice del DataFrame. El argumento inplace=True modifica el DataFrame directamente.
                # Un índice de tipo datetime es ESENCIAL para funciones como .resample().
                self._df.set_index('fecha_hora', inplace=True)
                print("Columna 'fecha_hora' convertida y establecida como índice.")
            except Exception as e:
                # Manejo de errores si la conversión o el establecimiento del índice fallan, permitiendo que el programa continúe.
                print(f"Error al convertir o establecer la columna 'fecha_hora' como índice: {e}")
                print("Continuando sin establecer 'fecha_hora' como índice.")
        return self._df

    def mostrar_df(self):
        # Devuelve el DataFrame almacenado en la instancia de la clase.
        return self._df

    def info(self,op):
        # Muestra información básica (op=1) o técnica (op!=1) del DataFrame.
        if op == 1:
        # Devuelve un string con el número de registros y las columnas (variables).
            return f'> Registros cargados: {self._df.shape[0]}\n> Variables medidas: {len(self._df.columns)} variables ---> {", ".join(self._df.columns)}\n'
        else:
        # self._df.info(): Muestra un resumen técnico del DataFrame (tipos de datos, conteo de no-nulos, uso de memoria).
            return self._df.info()

    def estadisticas_df(self):
        # Calcula estadísticas descriptivas para todas las columnas numéricas del DataFrame.
        estadisticas = self._df.describe()
        # .rename(index=...): Renombra los índices del resultado de .describe() (ej: 'mean' a 'media') a español.
        # inplace=True modifica el DataFrame 'estadisticas' directamente.
        estadisticas.rename(index={
            'count': 'conteo',
            'mean': 'media',
            'std': 'desviacion_estandar',
            'min': 'minimo',
            '25%': 'percentil_25',
            '50%': 'mediana',
            '75%': 'percentil_75',
            'max': 'maximo'
        }, inplace=True)
        # .rename(columns=...): Renombra los nombres de las columnas (variables de calidad del aire) a español.
        estadisticas.rename(columns={
            'pm25': 'Material Particulado 2.5',
            'pm10': 'Material Particulado 10',
            'no': 'Monóxido de Nitrógeno',
            'no2': 'Dióxido de Nitrógeno',
            'nox': 'Óxidos de Nitrógeno',
            'ozono': 'Ozono',
            'co': 'Monóxido de Carbono'
        }, inplace=True)
        return estadisticas

class ManejadorMat:
    """Clase para manipular de forma modular e independiente archivos .mat"""
    
    def __init__(self, ruta_archivo):
        # Guarda la ruta del archivo seleccionado para usarla en los métodos
        self.ruta = ruta_archivo
        self.datos = None
        self.info = None

    def cargar_archivo(self):
        """Carga el diccionario de datos del archivo .mat"""
        try:
            # sio.loadmat convierte el archivo .mat en un diccionario de Python
            self.datos = sio.loadmat(self.ruta)
            # sio.whosmat extrae los metadatos (nombres, dimensiones y tipo) sin cargar todo el peso
            self.info = sio.whosmat(self.ruta)
            return True
        except Exception as e:
            # En caso de error (archivo corrupto o no encontrado), avisa al usuario
            print(f"Error al cargar: {e}")
            return False
        
    def obtener_info_llaves(self):
            """Devuelve la información de las llaves (nombre, tamaño, tipo)"""
            # Retorna la lista con los metadatos obtenida por whosmat
            return self.info

    def obtener_matriz_principal(self):
        """Extrae la primera matriz de datos detectada"""
        if self.info and self.datos:
            # info[0][0] extrae el nombre de la primera variable guardada en el archivo .mat
            llave_principal = self.info[0][0]
            # Retorna el contenido (la matriz numérica) asociada a esa llave
            return self.datos[llave_principal]
        return None
    