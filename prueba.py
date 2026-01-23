import pandas as pd
import pywhatkit
import time

# --- CONFIGURACIÓN ---
# 1. Pega aquí el enlace que copiaste al "Publicar en la web" de Google Sheets
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8GptzYyGiULyjqQ188poL8yx2w0wjgpEicFH_FvxJCwcsTBlI9fpK4fkdKAS3TnPcYW5YWTmYI7GA/pub?output=csv"

def revisar_google_sheets():
    try:
        # Lee la hoja de Google Sheets directamente de internet
        df = pd.read_csv(URL_GOOGLE_SHEET)
        
        # Buscamos: Estado sea 'Confirmada' Y Enviado NO sea 'SI'
        filas_a_notificar = df[(df['Estado'] == 'Confirmada') & (df['Enviado'] != 'SI')]

        if filas_a_notificar.empty:
            print("No hay citas confirmadas nuevas por enviar.")
            return

        for index, fila in filas_a_notificar.iterrows():
            nombre = fila['Nombre']
            telefono = str(fila['Telefono'])
            
            # Mensaje personalizado con el nombre
            mensaje = f"Hola {nombre}, ¡tu cita ha sido CONFIRMADA con éxito! Te esperamos."

            print(f"Enviando confirmación a {nombre}...")
            
            # Envía el mensaje
            pywhatkit.sendwhatmsg_instantly(telefono, mensaje, wait_time=15, tab_close=True)
            
            print(f"✅ Mensaje enviado a {nombre}. Recuerda marcar manualmente 'SI' en la columna Enviado de tu Sheet.")
            
            # Espera para no saturar WhatsApp
            time.sleep(10)

    except Exception as e:
        print(f"Error al leer la hoja: {e}")

# --- INICIO DEL PROGRAMA ---
print("Sistema de Vigilancia de Google Sheets Activado...")
while True:
    revisar_google_sheets()
    # Revisa la hoja cada 60 segundos
    time.sleep(60)
