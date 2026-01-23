import pandas as pd
import pywhatkit
import time
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. ARREGLO PARA MAC (SSL)
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN ---
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8GptzYyGiULyjqQ188poL8yx2w0wjgpEicFH_FvxJCwcsTBlI9fpK4fkdKAS3TnPcYW5YWTmYI7GA/pub?output=csv" # El que termina en output=csv

def iniciar_sistema_potente():
    print("🚀 Iniciando Motor de WhatsApp...")
    
    # Configurar Navegador para Selenium (Vigía)
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./User_Data") # Guarda tu sesión de WhatsApp
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")
    
    print("⏳ Tienes 20 segundos para escanear el QR o esperar a que cargue...")
    time.sleep(20)

    while True:
        try:
            # --- FASE 1: ENVIAR NOTIFICACIONES/OFERTAS ---
            print("revisando Google Sheets para nuevos envíos...")
            df = pd.read_csv(URL_CSV)
            df.columns = df.columns.str.strip()

            # Buscar filas para enviar (Estado='Confirmada' y Enviado != 'SI')
            pendientes = df[(df['Estado'] == 'Confirmada') & (df['Enviado'] != 'SI')]

            for index, fila in pendientes.iterrows():
                nombre = fila['Nombre']
                tel = str(fila['Telefono']).strip()
                if not tel.startswith('+'): tel = '+' + tel
                
                mensaje = f"Hola {nombre}, ¡cita confirmada! 🌟 Por cierto, hoy tenemos una PROMO especial. ¿Te interesa recibir la guía gratuita? Responde 'PROMO'."
                
                print(f"Enviando mensaje inicial a {nombre}...")
                pywhatkit.sendwhatmsg_instantly(tel, mensaje, 15, True)
                print(f"✅ Enviado. No olvides marcar SI en tu Sheet manualmente.")
                time.sleep(10)

            # --- FASE 2: VIGILAR RESPUESTAS Y FILTRAR INTENCIÓN ---
            print("👀 Vigilando respuestas de clientes...")
            # Buscamos burbujas de mensajes no leídos (clase CSS de WhatsApp Web)
            nuevos_mensajes = driver.find_elements(By.XPATH, "//span[@aria-label='Unread']")
            
            for chat in nuevos_mensajes:
                chat.click() # Entrar al chat
                time.sleep(2)
                
                # Leer el último texto enviado por el cliente
                textos = driver.find_elements(By.CLASS_NAME, "copyable-text")
                if textos:
                    ultimo_texto = textos[-1].text.upper()
                    
                    # FILTRADO DE INTENCIONES (Lead Magnet)
                    if "PROMO" in ultimo_texto or "GUIA" in ultimo_texto:
                        print("🔥 ¡LEAD MAGNET DETECTADO!")
                        respuesta_bot = "¡Genial! Aquí tienes tu regalo: https://tu-enlace-aqui.com 🎁"
                        
                        # Escribir respuesta en WhatsApp
                        caja_texto = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                        caja_texto.send_keys(respuesta_bot + Keys.ENTER)
                        
                        print("✅ Lead Magnet enviado automáticamente.")

            time.sleep(30) # Esperar antes de la siguiente revisión general

        except Exception as e:
            print(f"Error en el ciclo: {e}")
            time.sleep(10)

# Lanzar el sistema
iniciar_sistema_potente()
