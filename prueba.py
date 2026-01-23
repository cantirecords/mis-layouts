import pandas as pd
import pywhatkit
import time

# --- CONFIGURACIÓN ---
# Pega aquí el link que obtuviste al "Publicar en la web" (el que termina en .csv)
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT8GptzYyGiULyjqQ188poL8yx2w0wjgpEicFH_FvxJCwcsTBlI9fpK4fkdKAS3TnPcYW5YWTmYI7GA/pubhtml"

def revisar_y_enviar():
    print("Conectando con Google Sheets...")
    try:
        # 1. Leer la hoja desde internet
        df = pd.read_csv(URL_GOOGLE_SHEET)
        
        # 2. Buscar clientes con Estado 'Confirmada' y que no se hayan enviado ('SI')
        # Nota: Asegúrate de que en tu Excel escribiste 'Confirmada' y 'Enviado' exactamente así
        pendientes = df[(df['Estado'] == 'Confirmada') & (df['Enviado'] != 'SI')]

        if pendientes.empty:
            print("No hay citas confirmadas nuevas por ahora.")
            return

        for index, fila in pendientes.iterrows():
            nombre = fila['Nombre']
            telefono = str(fila['Telefono'])
            
            # Si el teléfono no tiene el +, se lo agregamos automáticamente
            if not telefono.startswith('+'):
                telefono = '+' + telefono
            
            mensaje = f"Hola {nombre}, ¡tu cita ha sido CONFIRMADA! Nos vemos pronto."

            print(f"Enviando mensaje a {nombre}...")
            
            # Abrir WhatsApp y enviar
            pywhatkit.sendwhatmsg_instantly(telefono, mensaje, wait_time=15, tab_close=True)
            
            print(f"✅ Enviado a {nombre}. ¡No olvides poner 'SI' en tu Google Sheet!")
            time.sleep(10)

    except Exception as e:
        print(f"Error: {e}")

# Ejecutar la revisión
revisar_y_enviar()
