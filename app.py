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
