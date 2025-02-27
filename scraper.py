import requests
from bs4 import BeautifulSoup
import re
import time

def obtener_precio(html):
    """ Extrae el precio del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        precio_element = soup.find('div', {'class': re.compile('.*_tyxjp1.*')})
        if precio_element:
            return precio_element.text.strip()
        return "No disponible"
    except:
        return "No disponible"


def obtener_caracteristicas(html):
    """ Extrae características destacadas del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        caracteristicas = []
        for item in soup.find_all('div', {'class': re.compile('.*_1dotkqq.*')}):
            caracteristicas.append(item.text.strip())
        return caracteristicas if caracteristicas else ["No disponibles"]
    except:
        return ["No disponibles"]

def obtener_fotos(html):
    """ Extrae las URLs de las fotos del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        fotos = []
        for img in soup.find_all('img'):
            src = img.get('data-src') or img.get('src')
            if src and 'airbnb' in src:
                fotos.append(src)
        return fotos[:5] if fotos else ["No disponibles"]
    except:
        return ["No disponibles"]

def obtener_resenas(html):
    """ Extrae las reseñas más recientes del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        resenas = []
        for resena in soup.find_all('span', {'class': re.compile('.*_a7a5sx.*')}):
            resenas.append(resena.text.strip())
        return resenas[:3] if resenas else ["No hay reseñas disponibles"]
    except:
        return ["No hay reseñas disponibles"]

def obtener_competencia(zona):
    """ Obtiene precios de la competencia en la misma zona. """
    try:
        url_busqueda = f"https://www.airbnb.com/s/{zona}/homes"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_busqueda, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(response.text, 'html.parser')

        precios = []
        for precio in soup.find_all('span', {'class': re.compile(r'\$[0-9]+')}):
            precio_texto = precio.text.replace('$', '').strip()
            if precio_texto.isdigit():
                precios.append(int(precio_texto))

        if not precios:
            return "No disponible", "No disponible"

        precio_promedio = sum(precios) / len(precios)
        ocupacion_promedio = 75  

        return precio_promedio, ocupacion_promedio
    except Exception as e:
        return "Error obteniendo competencia", "Error obteniendo competencia"

def verificar_conexion(url):
    """ Prueba la conexión con Airbnb con cabeceras avanzadas para evitar bloqueos. """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive"
    }
    
    response = requests.get(url, headers=headers)
    
    print("Código de respuesta:", response.status_code)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Imprime los primeros 2000 caracteres del HTML
    print("HTML recibido:", response.text[:2000])
    
    # Prueba si hay un <h1> en el HTML
    titulo_h1 = soup.find('h1')
    if titulo_h1:
        print("Título encontrado en <h1>:", titulo_h1.text.strip())
    else:
        print("No se encontró ningún <h1> en el HTML.")

# -------------------- SELENIUM --------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def obtener_titulo(url):
    """ Usa Selenium para obtener el título de un anuncio en Airbnb. """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Configurar el driver para Render
    options.binary_location = "/usr/bin/google-chrome-stable"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)

    # ⏳ Esperar para permitir que el contenido cargue
    time.sleep(5)

    # 🔽 Forzar el scroll para cargar contenido dinámico de Airbnb
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        titulo_element = driver.find_element(By.TAG_NAME, "h1")
        titulo = titulo_element.text.strip()
        print("Título encontrado:", titulo)  # 🟢 Mensaje de depuración para los logs
    except Exception as e:
        titulo = "No disponible"
        print("Error obteniendo título:", str(e))  # 🛑 Captura errores en los logs

    driver.quit()
    return titulo
