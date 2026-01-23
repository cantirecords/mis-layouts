import pandas as pd
import pywhatkit
import time
import ssl

# Solución para el error de certificados en Mac
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN ---
# Tu link ya convertido a formato CSV para que Python lo lea correctamente
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8GptzYyGiULyjqQ188poL8yx2w0wjgpEicFH_FvxJCwcsTBlI9fpK4fkdKAS3TnPcYW5YWTmYI7GA/pub?output=csv"

def revisar_google_sheets():
    try:
        # Leemos la hoja saltando las filas que tengan errores (como la línea 65)
        df = pd.read_csv(URL_GOOGLE_SHEET, on_bad_lines='skip')
        
        # Limpiamos los nombres de las columnas (quita espacios extra)
        df.columns = df.columns.str.strip()
        
        # Verificamos que las columnas necesarias existan
        columnas_req = ['Nombre', 'Telefono', 'Estado', 'Enviado']
        if not all(col in df.columns for col in columnas_req):
            print(f"❌ Error: Revisa los títulos en tu Sheet. Columnas leídas: {list(df.columns)}")
            return

        # Convertimos todo a texto para comparar sin errores
        df['Estado'] = df['Estado'].astype(str).str.strip()
        df['Enviado'] = df['Enviado'].astype(str).str.strip()

        # Buscamos: Estado sea 'Confirmada' y Enviado NO sea 'SI'
        pendientes = df[(df['Estado'] == 'Confirmada') & (df['Enviado'] != 'SI')]

        if pendientes.empty:
            print("Esperando... No hay nuevas confirmaciones pendientes en el Sheet.")
            return

        for index, fila in pendientes.iterrows():
            nombre = fila['Nombre']
            telefono = str(fila['Telefono']).strip()
            
            if not telefono.startswith('+'):
                telefono = '+' + telefono

            mensaje = f"Hola {nombre}, ¡tu cita ha sido CONFIRMADA! Te esperamos pronto."

            print(f"🚀 Procesando a {nombre}...")
            
            # Envío automático
            pywhatkit.sendwhatmsg_instantly(telefono, mensaje, wait_time=15, tab_close=True)
            
            print(f"✅ Mensaje enviado a {nombre}. ¡Pon 'SI' en la columna Enviado de tu Sheet!")
            time.sleep(10)

    except Exception as e:
        print(f"❌ Error al procesar la hoja: {e}")

# --- INICIO DEL PROGRAMA ---
print("--- Sistema de Vigilancia Conectado y Blindado ---")
while True:
    revisar_google_sheets()
    # Revisa la hoja cada 30 segundos
    time.sleep(30)
