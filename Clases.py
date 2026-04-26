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


def graficar_suma_canales(self, ch1, ch2, ch3, p_min, p_max, fs=1000):
      """Suma 3 canales de una matriz y grafica el resultado en un segmento específico.

      Args:
          ch1, ch2, ch3 (int): Índices de los canales a sumar (0-basado).
          p_min (int): Punto mínimo (muestra inicial) para el segmento a analizar.
          p_max (int): Punto máximo (muestra final) para el segmento a analizar.
          fs (int): Frecuencia de muestreo (por defecto 1000 Hz).
      """
      if self.datos is None or self.info is None:
          print("Error: El archivo .mat no ha sido cargado. Use 'cargar_archivo()' primero.")
          return

      matriz = self.obtener_matriz_principal()
      if matriz is None:
          print("Error: No se pudo obtener la matriz principal del archivo.")
          return

      # Convertir a 2D si es 3D
      matriz_2d = matriz
      if matriz.ndim == 3:
          print(f"Detectada matriz 3D {matriz.shape}. Convirtiendo a 2D (Canales x Tiempo)...")
          matriz_2d = matriz[:, :, 0] # Toma el primer 'slice' si es 3D

      print(f"El archivo tiene {matriz_2d.shape[0]} canales.")

      # Procesamiento
      indices = [ch1, ch2, ch3]
      # Asegurar que los índices y el rango de puntos sean válidos
      if not all(0 <= idx < matriz_2d.shape[0] for idx in indices):
          print("Error: Índices de canal fuera de rango.")
          return
      if not (0 <= p_min < matriz_2d.shape[1] and 0 <= p_max < matriz_2d.shape[1] and p_min < p_max):
          print("Error: Puntos mínimo o máximo fuera de rango o inválidos.")
          return

      segmentos = matriz_2d[indices, p_min:p_max]
      suma_result = np.sum(segmentos, axis=0)

      tiempo = np.arange(p_min, p_max) / fs

      # Graficar
      fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

      for i, idx in enumerate(indices):
          ax1.plot(tiempo, segmentos[i, :], label=f'Canal {idx}')
      ax1.set_title(f"Canales seleccionados de {os.path.basename(self.ruta)}")
      ax1.set_ylabel("Amplitud (µV)")
      ax1.legend()

      ax2.plot(tiempo, suma_result, color='black', label='Suma de canales')
      ax2.set_title("Resultado de la Operación (Suma)")
      ax2.set_xlabel("Tiempo (s)")
      ax2.set_ylabel("Amplitud (µV)")
      ax2.legend()

      plt.tight_layout()
      nombre_grafico = f"resultado_{os.path.basename(self.ruta)[:-4]}.png"
      plt.savefig(nombre_grafico)
      print(f"Gráfico guardado como: {nombre_grafico}")
      plt.show()

def graficar_promedio_desviacion(self, eje):
        """Calcula y grafica el promedio y la desviación estándar de la matriz a lo largo de un eje específico.

        Args:
            eje (int): Eje a lo largo del cual calcular el promedio y la desviación estándar (0, 1 o 2 para 3D).
        """
        if self.datos is None or self.info is None:
            print("Error: El archivo .mat no ha sido cargado. Use 'cargar_archivo()' primero.")
            return

        matriz = self.obtener_matriz_principal()
        if matriz is None:
            print("Error: No se pudo obtener la matriz principal del archivo.")
            return

        if not (0 <= eje < matriz.ndim): # Valida que el eje sea válido para las dimensiones de la matriz.
            print(f"Error: El eje {eje} no es válido para una matriz de {matriz.ndim} dimensiones.")
            return

        print(f"Dimensiones de la matriz original: {matriz.shape}")

        promedio = np.mean(matriz, axis=eje)
        desviacion = np.std(matriz, axis=eje)

        # Si el resultado del promedio/desviación es una matriz 2D, se promedia nuevamente para obtener 1D.
        promedio_final = promedio
        std_final = desviacion

        if promedio.ndim > 1:
            promedio_final = np.mean(promedio, axis=0) # Promedia a lo largo del primer eje restante para hacerlo 1D.
        if desviacion.ndim > 1:
            std_final = np.mean(desviacion, axis=0) # Promedia a lo largo del primer eje restante para hacerlo 1D.

        # Graficar con Stem
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

        ax1.stem(promedio_final, linefmt='b-', markerfmt='bo', basefmt='r-')
        ax1.set_title("Promedio a lo largo del eje seleccionado")
        ax1.set_ylabel("Media")

        ax2.stem(std_final, linefmt='g-', markerfmt='go', basefmt='r-')
        ax2.set_title("Desviación Estándar a lo largo del eje seleccionado")
        ax2.set_ylabel("Desviación")
        ax2.set_xlabel("Muestras")

        plt.tight_layout()
        plt.show()
    