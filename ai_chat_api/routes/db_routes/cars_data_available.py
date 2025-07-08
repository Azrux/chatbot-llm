import os
import pandas as pd

# Leer el archivo CSV

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), '..', '..', '..', 'sample_caso_ai_engineer.csv')


def get_makes():
    """
    Lee un archivo CSV y obtiene las marcas únicas de la columna 'make'.
    Imprime las marcas ordenadas alfabéticamente.
    """
    try:
        df = pd.read_csv(CSV_PATH)

        # Verificar si existe la columna 'make'
        if 'make' in df.columns:
            # Obtener valores únicos de la columna 'make'
            marcas_unicas = df['make'].dropna().unique()

            # Ordenar alfabéticamente
            marcas_unicas = sorted(marcas_unicas)

            print(f"Total de marcas únicas encontradas: {len(marcas_unicas)}")
            print("\nMarcas disponibles:")
            print("-" * 30)

            for i, marca in enumerate(marcas_unicas, 1):
                print(f"{i:2d}. {marca}")

            return marcas_unicas

        else:
            print("Error: No se encontró la columna 'make' en el archivo CSV")
            print("Columnas disponibles:", list(df.columns))
            return []

    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV")
        print("Asegúrate de que el archivo esté en el mismo directorio y cambia 'tu_archivo.csv' por el nombre correcto")
        return []
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return []


def get_models():
    """
    Lee un archivo CSV y obtiene los modelos únicos de la columna 'model'.
    Imprime los modelos ordenados alfabéticamente.
    """
    try:
        df = pd.read_csv(CSV_PATH)

        # Verificar si existe la columna 'model'
        if 'model' in df.columns:
            # Obtener valores únicos de la columna 'model'
            modelos_unicos = df['model'].dropna().unique()

            # Ordenar alfabéticamente
            modelos_unicos = sorted(modelos_unicos)

            print(
                f"Total de modelos únicos encontrados: {len(modelos_unicos)}")
            print("\nModelos disponibles:")
            print("-" * 30)

            for i, modelo in enumerate(modelos_unicos, 1):
                print(f"{i:2d}. {modelo}")

            return modelos_unicos

        else:
            print("Error: No se encontró la columna 'model' en el archivo CSV")
            print("Columnas disponibles:", list(df.columns))
            return []

    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV")
        print("Asegúrate de que el archivo esté en el mismo directorio y cambia 'tu_archivo.csv' por el nombre correcto")
        return []
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return []
