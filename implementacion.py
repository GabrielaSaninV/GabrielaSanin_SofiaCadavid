# Parcial 2
from Clases import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
import os
opciones_archivos = {
    1: 'CalAir_VA_2019.csv',
    2: 'CalAir_VA_2020.csv',
    3: 'CalAir_VA_2021.csv',
    4: 'CalAir_VA_2022.csv',
    5: 'CalAir_VA_2023.csv'
}
def main():
    while True:
        menuppal = int(input('Hola! Te encuentras en el sistema exploratorio para procesar archivos MAT de electroencefalografías y archivos CSV del SIATA\n¿Que deseas analizar?\n 1- Datos de la calidad del aire SIATA\n 2- Datos de EGG Parkinson\n 3-Salir\n'))
        if menuppal == 1:
            while True:
                opcion = int(input('Bienvenido al Sistema de Calidad de Aire!\nEscoja el año de los datos que desea visualizar:\n 1- 2019\n 2- 2020\n 3- 2021\n 4- 2022\n 5- 2023\n 6- Salir del menu\n'))
                if opcion == 6:
                    break # Sale del programa (bucle principal).

                # Verifica si la opción elegida corresponde a un archivo en 'opciones_archivos'.
                elif opcion in opciones_archivos:
                    ruta = opciones_archivos[opcion]
                    calAir = CalAir(ruta) # Crea una instancia de la clase 'CalAir' con la ruta del archivo seleccionado.
                    calAir.cargar_df() # Llama al método 'cargar_df()' para cargar los datos y configurar el DataFrame.
                    print('Archivo cargado exitosamente')

                    # Submenú: Una vez cargado el archivo, ofrece opciones para procesar y analizar los datos.
                    while True:
                        submenu = int(input(' 1- Mostrar información del archivo\n 2- Observar estadisticas del archivo\n 3- Graficar datos\n 4- Aplicar operación Apply\n 5- Aplicar operación Map (Categorización)\n 6- Sumar/Restar columnas\n 7- Remuestrear y Graficar Datos\n 8- Salir del menu\n'))
                        
                        if submenu == 1: # Opción para mostrar información del DataFrame (básica o técnica).
                            op = int(input('1- Visualización Básica\n2- Visualización Técnica\n'))
                            print(calAir.info(op))

                        elif submenu == 2: # Opción para observar las estadísticas descriptivas del DataFrame.
                            print(calAir.estadisticas_df())

                        elif submenu == 3: # Opción para graficar datos de una columna.
                            df_actual = calAir.mostrar_df() # Obtiene la versión más reciente del DataFrame.
                            if df_actual.empty:
                                print("No hay datos cargados para graficar.")
                                continue

                            nombres_columnas = df_actual.columns.tolist() # Obtiene una lista con los nombres de todas las columnas.
                            print("Columnas disponibles:", nombres_columnas)
                            try:
                                # Solicita al usuario que seleccione una columna por su índice numérico (0-basado).
                                indice_columna = int(input(f'Seleccione el número de columna a graficar (0 para la primera, {len(nombres_columnas)-1} para la última): '))
                                # Valida que el índice ingresado esté dentro del rango de columnas.
                                if not (0 <= indice_columna < len(nombres_columnas)):
                                    print("Índice de columna no válido.")
                                    continue
                                # .iloc[:, indice_columna]: Selecciona todos los datos de la columna en la posición 'indice_columna'.
                                data = df_actual.iloc[:,indice_columna]
                            except ValueError:
                                print("Entrada inválida. Por favor, ingrese un número entero para el índice de columna.")
                                continue

                            punto_inicial = 0
                            punto_final = len(data) - 1
                            # Bucle para permitir al usuario definir un rango específico de índices para la gráfica.
                            while True:
                                try:
                                    punto_inicial_str = input(f'Ingrese el punto inicial para la gráfica (índice 0 a {len(data)-1}, deje vacío para empezar desde el inicio): ')
                                    if punto_inicial_str:
                                        punto_inicial = int(punto_inicial_str)
                                    else:
                                        punto_inicial = 0

                                    punto_final_str = input(f'Ingrese el punto final para la gráfica (índice 0 a {len(data)-1}, deje vacío para ir hasta el final): ')
                                    if punto_final_str:
                                        punto_final = int(punto_final_str)
                                    else:
                                        punto_final = len(data) - 1

                                    # Validación de los índices ingresados para asegurar que estén dentro de los límites y que 'inicial' no sea mayor que 'final'.
                                    if not (0 <= punto_inicial < len(data) and 0 <= punto_final < len(data)):
                                        print(f"Rangos inválidos. Los índices deben estar entre 0 y {len(data)-1}.")
                                    elif punto_inicial > punto_final:
                                        print("El punto inicial no puede ser mayor que el punto final.")
                                    else:
                                        break # Si los índices son válidos, sale del bucle de selección de rango.
                                except ValueError:
                                    print("Entrada inválida. Por favor, ingrese números enteros para los índices.")
                            
                            # Opción para guardar el gráfico generado como un archivo de imagen.
                            guardar_grafico = input("¿Desea guardar el gráfico? (s/n): ").lower()
                            save_path = None
                            if guardar_grafico == 's':
                                nombre_archivo = input("Ingrese el nombre del archivo (ej: mi_grafico.png): ")
                                save_path = nombre_archivo

                            calAir.graficar_df(data, indice_inicio=punto_inicial, indice_fin=punto_final, save_path=save_path) # Llama al método de graficación de la clase.

                        elif submenu == 4: # Opción para aplicar operaciones 'apply' (cuadrado, raíz cuadrada).
                            print("\n--- Operación Apply ---")
                            df_actual = calAir.mostrar_df()
                            if df_actual.empty:
                                print("No hay datos cargados para operar.")
                                continue

                            # Se filtran las columnas numéricas para asegurar que la operación sea válida.
                            columnas_numericas = [col for col in df_actual.columns if pd.api.types.is_numeric_dtype(df_actual[col])]
                            print("Columnas numéricas disponibles:", columnas_numericas)
                            if not columnas_numericas:
                                print("No hay columnas numéricas para aplicar esta operación.")
                                continue
                            columna_apply = input("Ingrese el nombre de la columna para aplicar 'apply': ")
                            if columna_apply not in columnas_numericas:
                                print("Columna no válida o no numérica.")
                                continue

                            print("Operaciones disponibles:")
                            print("1- Cuadrado (x^2)")
                            print("2- Raíz Cuadrada (sqrt(x))")
                            eleccion_operacion = input("Elija una operación (1 o 2): ")

                            func_name = None
                            if eleccion_operacion == '1':
                                func_name = 'cuadrado'
                                nombre_nueva_columna = f"{columna_apply}_cuadrado"
                            elif eleccion_operacion == '2':
                                func_name = 'raiz_cuadrada'
                                nombre_nueva_columna = f"{columna_apply}_raiz"
                            else:
                                print("Opción de operación no válida.")
                                continue

                            result_df_head = calAir.aplicar_operacion_apply(columna_apply, func_name, nombre_nueva_columna)
                            if result_df_head is not None:
                                # Muestra las primeras 5 filas de las columnas afectadas para una verificación rápida.
                                print("Resultados de las primeras 5 filas:")
                                print(result_df_head)
                                print(f"Nueva columna '{nombre_nueva_columna}' creada.")

                        elif submenu == 5: # Opción para aplicar operaciones 'map' (categorización con pd.cut).
                            print("\n--- Operación Map (Categorización) ---")
                            df_actual = calAir.mostrar_df()
                            if df_actual.empty:
                                print("No hay datos cargados para operar.")
                                continue

                            # Se filtran las columnas numéricas que pueden ser categorizadas.
                            columnas_numericas = [col for col in df_actual.columns if pd.api.types.is_numeric_dtype(df_actual[col])]
                            print("Columnas numéricas disponibles para categorización:", columnas_numericas)
                            if not columnas_numericas:
                                print("No hay columnas numéricas para aplicar esta operación.")
                                continue
                            columna_map = input("Ingrese el nombre de la columna para categorizar (ej: 'pm25' o 'co'): ")
                            if columna_map not in columnas_numericas:
                                print("Columna no válida o no numérica.")
                                continue

                            print("Categorizaciones disponibles:")
                            print("1- Nivel de PM2.5 (basado en estándares de calidad del aire)")
                            print("2- Nivel de CO (basado en estándares de calidad del aire)")
                            eleccion_operacion = input("Elija una categorización (1 o 2): ")

                            func_name = None
                            if eleccion_operacion == '1':
                                func_name = 'nivel_pm25'
                                nombre_nueva_columna = f"{columna_map}_nivel"
                            elif eleccion_operacion == '2':
                                func_name = 'clasificar_co'
                                nombre_nueva_columna = f"{columna_map}_clasificacion"
                            else:
                                print("Opción de categorización no válida.")
                                continue

                            result_df_head = calAir.aplicar_operacion_map(columna_map, func_name, nombre_nueva_columna)
                            if result_df_head is not None:
                                # Muestra las primeras 5 filas para verificar la nueva columna categorizada.
                                print("Resultados de las primeras 5 filas:")
                                print(result_df_head)
                                print(f"Nueva columna '{nombre_nueva_columna}' creada.")

                        elif submenu == 6: # Opción para sumar o restar dos columnas.
                            print("\n--- Operar Columnas ---")
                            df_actual = calAir.mostrar_df()
                            if df_actual.empty:
                                print("No hay datos cargados para operar.")
                                continue

                            # Se listan las columnas numéricas disponibles para operaciones aritméticas.
                            columnas_numericas = [col for col in df_actual.columns if pd.api.types.is_numeric_dtype(df_actual[col])]
                            print("Columnas numéricas disponibles:", columnas_numericas)
                            if len(columnas_numericas) < 2:
                                print("Se necesitan al menos dos columnas numéricas para esta operación.")
                                continue

                            columna1 = input("Ingrese el nombre de la primera columna: ")
                            columna2 = input("Ingrese el nombre de la segunda columna: ")
                            if columna1 not in columnas_numericas or columna2 not in columnas_numericas:
                                print("Una o ambas columnas no son válidas o no son numéricas.")
                                continue

                            operacion = input("¿Qué operación desea realizar? (suma/resta): ").lower()
                            nombre_nueva_columna = input("Ingrese el nombre para la nueva columna resultante (ej: 'pm_diff'): ")

                            result_df_head = calAir.operar_columnas(columna1, columna2, operacion, nombre_nueva_columna)
                            if result_df_head is not None:
                                # Muestra las primeras 5 filas de las columnas involucradas y la nueva.
                                print("Resultados de las primeras 5 filas:")
                                print(result_df_head)
                                print(f"Nueva columna '{nombre_nueva_columna}' creada.")

                        elif submenu == 7: # Opción para remuestrear y graficar datos de series temporales.
                            print("\n--- Remuestrear y Graficar Datos ---")
                            df_actual = calAir.mostrar_df()
                            if df_actual.empty:
                                print("No hay datos cargados para remuestrear.")
                                continue
                            # Validación crucial: se asegura de que el índice del DataFrame sea de tipo DatetimeIndex, necesario para .resample().
                            if not isinstance(df_actual.index, pd.DatetimeIndex):
                                print("El DataFrame no tiene un índice de tipo fecha y hora. Por favor, asegúrese de que 'fecha_hora' se haya establecido como índice.")
                                continue

                            # Se listan las columnas numéricas disponibles para remuestreo.
                            columnas_numericas = [col for col in df_actual.columns if pd.api.types.is_numeric_dtype(df_actual[col])]
                            print("Columnas numéricas disponibles para remuestreo:", columnas_numericas)
                            if not columnas_numericas:
                                print("No hay columnas numéricas para aplicar esta operación.")
                                continue
                            columna_resample = input("Ingrese el nombre de la columna a remuestrear y graficar: ")
                            if columna_resample not in columnas_numericas:
                                print("Columna no válida o no numérica.")
                                continue

                            print("Frecuencias de remuestreo disponibles:")
                            print("1- Diaria (D)")
                            print("2- Mensual (M)")
                            print("3- Trimestral (Q)")
                            eleccion_frecuencia = int(input("Elija una frecuencia (1, 2 o 3): "))

                            frecuencia = None
                            if eleccion_frecuencia == 1:
                                frecuencia = 'D'
                            elif eleccion_frecuencia == 2:
                                frecuencia = 'M'
                            elif eleccion_frecuencia == 3:
                                frecuencia = 'Q'
                            else:
                                print("Opción de frecuencia no válida.")
                                continue

                            # Opción para guardar el gráfico remuestreado.
                            guardar_grafico = input("¿Desea guardar el gráfico remuestreado? (s/n): ").lower()
                            save_path = None
                            if guardar_grafico == 's':
                                nombre_archivo = input("Ingrese el nombre del archivo (ej: mi_grafico_resample.png): ")
                                save_path = nombre_archivo

                            calAir.remuestrear_y_graficar(columna_resample, frecuencia, save_path=save_path) # Llama al método de remuestreo y graficación.

                        elif submenu == 8:
                            break # Sale del submenú y regresa al menú principal de selección de archivo.
                        else:
                            print('Opción no válida, intente de nuevo') # Mensaje si la opción del submenú es inválida.

                else:
                    print("Opción no válida, intente de nuevo.") # Mensaje si la opción del menú principal es inválida.
        elif menuppal == 2:
            while True:
                archivos_disponibles = [f for f in os.listdir() if f.endswith('.mat')]
                if not archivos_disponibles:
                    print("No se encontraron archivos .mat en la carpeta actual.")
                    continue # Continuar el bucle para permitir al usuario salir o reintentar

                print("Archivos detectados:")
                for i, nombre in enumerate(archivos_disponibles):
                    print(f"{i+1}. {nombre}")

                try:
                    seleccion = int(input("Seleccione el número del archivo a cargar: ")) - 1
                    if not (0 <= seleccion < len(archivos_disponibles)):
                        print("Selección inválida. Por favor, ingrese un número dentro del rango.")
                        continue
                    nombre_archivo = archivos_disponibles[seleccion]
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un número.")
                    continue

                manejador = ManejadorMat(nombre_archivo)
                if not manejador.cargar_archivo(): # Cargar el archivo al inicio.
                    print(f"No se pudo procesar {nombre_archivo}. Seleccione otro archivo.")
                    continue

                print(f"\n--- Analizando: {nombre_archivo} ---")
                info = manejador.obtener_info_llaves()

                print("Llaves encontradas (whosmat):")
                for item in info:
                    print(f"Nombre: {item[0]}, Tamaño: {item[1]}, Tipo: {item[2]}")
                    
if __name__ == "__main__":
    main()