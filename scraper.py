import requests
from bs4 import BeautifulSoup
import re
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller  # 📌 Nueva importación para instalar ChromeDriver automáticamente

# 📌 Instalar automáticamente ChromeDriver en la versión correcta
chromedriver_autoinstaller.install()

# -------------------- BEAUTIFULSOUP --------------------

def obtener_precio(html):
    """ Extrae el precio del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        precio_element = soup.find('div', {'class': re.compile('.*_tyxjp1.*')})
        return precio_element.text.strip() if precio_element else "No disponible"
    except:
        return "No disponible"

def obtener_caracteristicas(html):
    """ Extrae características destacadas del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        caracteristicas = [item.text.strip() for item in soup.find_all('div', {'class': re.compile('.*_1dotkqq.*')})]
        return caracteristicas if caracteristicas else ["No disponibles"]
    except:
        return ["No disponibles"]

def obtener_fotos(html):
    """ Extrae las URLs de las fotos del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        fotos = [img.get('data-src') or img.get('src') for img in soup.find_all('img') if img.get('src') and 'airbnb' in img.get('src')]
        return fotos[:5] if fotos else ["No disponibles"]
    except:
        return ["No disponibles"]

def obtener_resenas(html):
    """ Extrae las reseñas más recientes del anuncio. """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        resenas = [resena.text.strip() for resena in soup.find_all('span', {'class': re.compile('.*_a7a5sx.*')})]
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

        precios = [int(precio.text.replace('$', '').strip()) for precio in soup.find_all('span', {'class': re.compile(r'\$[0-9]+')}) if precio.text.replace('$', '').strip().isdigit()]
        
        if not precios:
            return "No disponible", "No disponible"

        return sum(precios) / len(precios), 75  # Ocupación estimada
    except:
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
    print("HTML recibido:", response.text[:2000])  # Depuración

    titulo_h1 = soup.find('h1')
    print("Título encontrado en <h1>:", titulo_h1.text.strip() if titulo_h1 else "No se encontró ningún <h1> en el HTML.")

# -------------------- SELENIUM --------------------

def obtener_titulo(url):
    """ Usa Selenium para obtener el título de un anuncio en Airbnb. """
    print("\n🔍 Iniciando Selenium para obtener título...\n")
    sys.stdout.flush()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en segundo plano
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 📌 Configurar Chrome para Render
    import os  # 📌 Importar el módulo para leer variables de entorno
options.binary_location = os.getenv("GOOGLE_CHROME_BIN", "/opt/render/chrome/chrome")


    # 📌 Inicializar ChromeDriver correctamente
driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH", "/opt/render/chromedriver/chromedriver"), options=options)


    print("✅ Navegador Chrome iniciado correctamente.")
    sys.stdout.flush()

    driver.get(url)
    print(f"🌐 URL cargada en el navegador: {url}")
    sys.stdout.flush()

    # Esperar a que el contenido cargue completamente
    time.sleep(5)

    # Desplazamiento para cargar contenido dinámico
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        print("🔎 Buscando el título en la página...")
        sys.stdout.flush()

        titulo_element = driver.find_element(By.TAG_NAME, "h1")
        titulo = titulo_element.text.strip()
        print(f"✅ Título encontrado: {titulo}")
    
    except Exception as e:
        titulo = "No disponible"
        print(f"❌ Error obteniendo título: {str(e)}")
    
    sys.stdout.flush()
    
    driver.quit()
    print("🚪 Navegador cerrado.")
    sys.stdout.flush()

    return titulo
