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