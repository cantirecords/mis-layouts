import pandas as pd
import pywhatkit
import time
import ssl

# Arreglo para el error de certificado en Mac
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN ---
# Tu link de Google Sheets (el que termina en .csv)
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8GptzYyGiULyjqQ188poL8yx2w0wjgpEicFH_FvxJCwcsTBlI9fpK4fkdKAS3TnPcYW5YWTmYI7GA/pubhtml"

def revisar_google_sheets():
    try:
        # 1. Leer la hoja
        df = pd.read_csv(URL_GOOGLE_SHEET)
        
        # LIMPIEZA: Quita espacios en blanco de los títulos
        df.columns = df.columns.str.strip()
        
        # Verificamos si la columna existe antes de seguir
        if 'Estado' not in df.columns:
            print(f"❌ Error: No encuentro la columna 'Estado'. Columnas detectadas: {list(df.columns)}")
            return

        # 2. Buscar citas: Estado es 'Confirmada' y Enviado NO es 'SI'
        # Convertimos todo a texto para evitar errores
        df['Estado'] = df['Estado'].astype(str).str.strip()
        df['Enviado'] = df['Enviado'].astype(str).str.strip()

        pendientes = df[(df['Estado'] == 'Confirmada') & (df['Enviado'] != 'SI')]

        if pendientes.empty:
            print("Esperando... No hay citas nuevas para enviar.")
            return

        for index, fila in pendientes.iterrows():
            nombre = fila['Nombre']
            telefono = str(fila['Telefono']).strip()
            
            # Si el número no tiene el +, se lo ponemos
            if not telefono.startswith('+'):
                telefono = '+' + telefono

            mensaje = f"Hola {nombre}, ¡tu cita ha sido CONFIRMADA! Nos vemos pronto."

            print(f"🚀 Enviando mensaje a {nombre} al número {telefono}...")
            
            # Enviar mensaje
            pywhatkit.sendwhatmsg_instantly(telefono, mensaje, wait_time=15, tab_close=True)
            
            print(f"✅ ¡Éxito! Recuerda poner 'SI' en la columna Enviado de tu Sheet.")
            time.sleep(10)

    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# --- INICIO ---
print("--- Sistema de Vigilancia Iniciado ---")
while True:
    revisar_google_sheets()
    time.sleep(30) # Revisa cada 30 segundos
