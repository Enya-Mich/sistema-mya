# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql://mi_usuario:mi_contraseña@localhost/mi_proyecto_db'




import requests

# URL base de la API de OpenWeatherMap
url_base = "http://api.openweathermap.org/data/2.5/weather?"

# Ciudad y clave de la API (reemplázalas con los valores correctos)
ciudad = "Lima"
clave_api = "TU_CLAVE_DE_API"

# Construye la URL completa para la consulta
url = f"{url_base}q={ciudad}&appid={clave_api}"

# Realiza la solicitud a la API de OpenWeatherMap
response = requests.get(url)

# Comprueba si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convierte la respuesta a JSON
    datos_clima = response.json()

    # Extrae información relevante del JSON
    temperatura = datos_clima['main']['temp']
    descripcion = datos_clima['weather'][0]['description']

    # Imprime la información del clima
    print(f"Temperatura: {temperatura} K")
    print(f"Descripción: {descripcion}")
else:
    print("Error al obtener datos del clima.")

