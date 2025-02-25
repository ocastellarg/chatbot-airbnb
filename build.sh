#!/usr/bin/env bash
# Instalar Google Chrome y ChromeDriver sin sudo en Render

# Crear directorios locales para Chrome y ChromeDriver
mkdir -p ~/chrome ~/chromedriver

# Descargar e instalar Google Chrome desde fuente alternativa
wget -q -O ~/chrome/chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
dpkg -x ~/chrome/chrome.deb ~/chrome/
export CHROME_PATH="$HOME/chrome/opt/google/chrome/chrome"
chmod +x $CHROME_PATH

# Verificar instalación de Chrome
$CHROME_PATH --version || echo "Error instalando Google Chrome"

# Descargar e instalar ChromeDriver desde fuente alternativa
wget -q -O ~/chromedriver/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chromedriver-linux64.zip"
unzip ~/chromedriver/chromedriver.zip -d ~/chromedriver/
export CHROMEDRIVER_PATH="$HOME/chromedriver/chromedriver-linux64/chromedriver"
chmod +x $CHROMEDRIVER_PATH

# Verificar instalación de ChromeDriver
$CHROMEDRIVER_PATH --version || echo "Error instalando ChromeDriver"
