from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def analizar_anuncio(url):
    """ Extrae y analiza datos clave del anuncio de Airbnb. """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer título del anuncio
        titulo = soup.find('h1').text if soup.find('h1') else "No disponible"

        # Extraer descripción
        descripcion = soup.find('meta', {'name': 'description'})
        descripcion = descripcion['content'] if descripcion else "No disponible"

        # Simulación de análisis (aquí puedes mejorar la lógica de análisis real)
        recomendaciones = []
        if len(titulo) < 30:
            recomendaciones.append("Tu título es muy corto. Intenta agregar palabras clave como 'Vista al mar' o 'Jacuzzi'.")
        if "wifi" not in descripcion.lower():
            recomendaciones.append("Considera mencionar si tienes WiFi rápido en la descripción.")

        return {"titulo": titulo, "descripcion": descripcion, "recomendaciones": recomendaciones}
    
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    url = request.form.get('url')  # Ahora obtiene la URL del formulario
    if not url:
        return render_template('index.html', error="Por favor, proporciona un enlace válido.")
    resultado = analizar_anuncio(url)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/test-conexion', methods=['GET'])
def test_conexion():
    url = "https://es-l.airbnb.com/rooms/1112472362544295200?guests=1&adults=1&s=67&unique_share_id=d55a289f-0e5e-4209-8318-c8d110ff1fbc"
    from scraper import verificar_conexion
    verificar_conexion(url)
    return "Verificación completada. Revisa los logs."
@app.route('/test-selenium', methods=['GET'])
def test_selenium():
    from scraper import obtener_titulo
    url = "https://www.airbnb.com/rooms/12345678"  # Reemplázalo con un enlace real de Airbnb
    titulo = obtener_titulo(url)
    return f"Título extraído: {titulo}"


