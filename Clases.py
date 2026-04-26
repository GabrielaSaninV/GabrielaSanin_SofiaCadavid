import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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