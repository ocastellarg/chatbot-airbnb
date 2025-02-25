#!/usr/bin/env bash
# Instalar Google Chrome y ChromeDriver en Render

# Actualizar paquetes
sudo apt-get update

# Instalar dependencias necesarias
sudo apt-get install -y wget unzip curl

# Descargar e instalar Google Chrome
wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome.deb || sudo apt-get -f install -y
rm google-chrome.deb

# Verificar instalación de Chrome
google-chrome --version

# Descargar e instalar ChromeDriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

# Verificar instalación de ChromeDriver
chromedriver --version
