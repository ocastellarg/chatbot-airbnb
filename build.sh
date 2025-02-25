#!/usr/bin/env bash
# Instalar Chromium y ChromeDriver en Render sin sudo

# Instalar Chromium en Render
apt update && apt install -y chromium-browser

# Verificar instalación de Chromium
CHROME_PATH=$(which chromium-browser)
if [ -z "$CHROME_PATH" ]; then
    echo "Error instalando Chromium"
else
    echo "Chromium instalado en: $CHROME_PATH"
fi

# Descargar e instalar ChromeDriver compatible con Chromium
mkdir -p ~/chromedriver
wget -q -O ~/chromedriver/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.105/linux64/chromedriver-linux64.zip"
unzip ~/chromedriver/chromedriver.zip -d ~/chromedriver/
export CHROMEDRIVER_PATH="$HOME/chromedriver/chromedriver-linux64/chromedriver"
chmod +x $CHROMEDRIVER_PATH

# Verificar instalación de ChromeDriver
$CHROMEDRIVER_PATH --version || echo "Error instalando ChromeDriver"

