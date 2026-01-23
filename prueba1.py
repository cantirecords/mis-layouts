import pandas as pd
import pywhatkit
import time
import ssl

# Arreglo para el error de certificado en Mac
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN ---
# He convertido tu link de 'pubhtml' a 'csv' para que Python lo entienda
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8GptzYyGiULyjqQ188poL8yx2w0wjgpEicFH_FvxJCwcsTBlI9fpK4fkdKAS3TnPcYW5YWTmYI7GA/pub?output=csv"

def revisar_google_sheets():
    try:
        # 1. Leer la hoja (usando el link CSV)
        df = pd.read_csv(URL_GOOGLE_SHEET)
        
        # Limpieza: quita espacios en los nombres de las columnas
        df.columns = df.columns.str.strip()
        
        # 2. Buscar: Estado es 'Confirmada' y Enviado NO es 'SI'
        # Convertimos a texto para que no haya errores de comparación
        df['Estado'] = df['Estado'].astype(str).str.strip()
        df['Enviado'] = df['Enviado'].astype(str).str.strip()

        pendientes = df[(df['Estado'] == 'Confirmada') & (df['Enviado'] != 'SI')]

        if pendientes.empty:
            print("Esperando... No hay citas confirmadas pendientes en tu Google Sheet.")
            return

        for index, fila in pendientes.iterrows():
            nombre = fila['Nombre']
            telefono = str(fila['Telefono']).strip()
            
            # Asegurar que el número tenga el +
            if not telefono.startswith('+'):
                telefono = '+' + telefono

            mensaje = f"Hola {nombre}, ¡tu cita ha sido CONFIRMADA! Nos vemos pronto."

            print(f"🚀 ¡Encontrado! Enviando mensaje a {nombre}...")
            
            # Enviar mensaje (espera 15 seg para cargar y cierra la pestaña)
            pywhatkit.sendwhatmsg_instantly(telefono, mensaje, wait_time=15, tab_close=True)
            
            print(f"✅ Éxito. Ahora escribe 'SI' en la columna Enviado de tu Sheet para {nombre}.")
            time.sleep(10)

    except Exception as e:
        print(f"❌ Error: {e}")

# --- INICIO ---
print("--- Sistema de Vigilancia Conectado a tu Google Sheet ---")
while True:
    revisar_google_sheets()
    time.sleep(30) # Revisa cada 30 segundos
