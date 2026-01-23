import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# --- CONFIGURACIÓN ---
URL_SHEET_CSV = "TU_LINK_CSV_AQUI"

def iniciar_robot():
    # 1. Configurar el navegador
    options = webdriver.ChromeOptions()
    # Esto guarda tu sesión para no escanear el QR cada vez
    options.add_argument("--user-data-dir=./User_Data") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://web.whatsapp.com")
    print("Por favor, escanea el código QR si es necesario...")
    
    # Esperamos a que cargue la interfaz (puedes subir este tiempo si tu internet es lento)
    time.sleep(20) 

    while True:
        try:
            # 2. Buscar chats con mensajes no leídos
            unread_chats = driver.find_elements(By.CLASS_NAME, "_ak8j") # Esta clase puede cambiar, es la de mensajes nuevos

            for chat in unread_chats:
                chat.click()
                time.sleep(2)
                
                # 3. Leer el último mensaje
                mensajes = driver.find_elements(By.CLASS_NAME, "copyable-text")
                ultimo_mensaje = mensajes[-1].text.upper() if mensajes else ""
                
                print(f"Mensaje recibido: {ultimo_mensaje}")

                # 4. FILTRADO DE INTENCIÓN
                if "PROMO" in ultimo_mensaje or "GUIA" in ultimo_mensaje:
                    print("🔥 ¡Lead Magnet detectado! Guardando en Sheets...")
                    # Aquí llamaríamos a una función para escribir en tu Google Sheet
                    # o simplemente responder automáticamente
                    responder_whatsapp(driver, "¡Genial! Aquí tienes tu guía: [LINK_DE_TU_REGALO]")

            time.sleep(10) # Revisa cada 10 segundos
        except Exception as e:
            print(f"Buscando mensajes nuevos... {e}")
            time.sleep(5)

def responder_whatsapp(driver, texto):
    input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    input_box.send_keys(texto + Keys.ENTER)

iniciar_robot()
