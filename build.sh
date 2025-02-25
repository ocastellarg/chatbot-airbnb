#!/usr/bin/env bash
# Instalar Google Chrome y ChromeDriver sin usar sudo en Render

# Crear un directorio local para Chrome
mkdir -p ~/chrome
cd ~/chrome

# Descargar e instalar Google Chrome (versión estable)
wget -q -O chrome-linux.zip "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
ar x chrome-linux.zip
tar -xf data.tar.xz
mv ./opt/google/chrome ./chrome
rm -rf *.deb *.zip *.tar.xz

# Configurar la variable de entorno para Chrome
export CHROME_PATH="$HOME/chrome/chrome"

# Verificar instalación de Chrome
$CHROME_PATH --version || echo "Error instalando Google Chrome"

# Descargar e instalar ChromeDriver
mkdir -p ~/chromedriver
cd ~/chromedriver
wget -q -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json | jq -r '.versions[-1].downloads.chromedriver[0].url')"
unzip chromedriver.zip
mv chromedriver-linux64/chromedriver ./chromedriver
chmod +x ./chromedriver

# Configurar l