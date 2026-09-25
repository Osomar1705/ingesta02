import boto3
import mysql.connector
import csv

# ---- Configuración MySQL ----
DB_HOST = "172.31.93.85"
DB_PORT = 8005
DB_USER = "root"
DB_PASSWORD = "utec"          # si tu password real es distinto, reemplázalo aquí
DB_NAME = "bd_api_employees"
TABLE_NAME = "employees"

# ---- Configuración S3 ----
ficheroUpload = "data.csv"
nombreBucket = "gcr-output-01"


def extraer_datos_mysql():
    conexion = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    filas = cursor.fetchall()
    nombres_columnas = [desc[0] for desc in cursor.description]

    with open(ficheroUpload, mode="w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(nombres_columnas)
        escritor.writerows(filas)

    cursor.close()
    conexion.close()
    print(f"Se exportaron {len(filas)} registros a {ficheroUpload}")


def subir_a_s3():
    s3 = boto3.client('s3')
    response = s3.upload_file(ficheroUpload, nombreBucket, "carpeta/" + ficheroUpload)
    print(response)
    print(f"Archivo {ficheroUpload} subido correctamente al bucket {nombreBucket}")


if __name__ == "__main__":
    extraer_datos_mysql()
    subir_a_s3()
    print("Ingesta completada")
