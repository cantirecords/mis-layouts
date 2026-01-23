import pywhatkit
import time

# --- CONFIGURACIÓN DE LA PRUEBA ---
# Escribe tu número con el signo + y tu código de país (ejemplo: +52 para México, +34 para España)
tu_numero = "+19012065004" 
mensaje_de_prueba = "¡Funciona! Este es un mensaje automático enviado desde Python 🐍"

print("Iniciando prueba en 5 segundos...")
time.sleep(5)

try:
    # Esta es la función mágica. 
    # wait_time=15: Espera 15 segundos a que cargue WhatsApp Web antes de escribir.
    # tab_close=True: Cierra la pestaña del navegador automáticamente después de enviar.
    print("Abriendo el navegador y preparando el envío...")
    
    pywhatkit.sendwhatmsg_instantly(
        phone_no=tu_numero, 
        message=mensaje_de_prueba,
        wait_time=15,
        tab_close=True
    )
    
    print("--------------------------------------------------")
    print("¡LISTO! Si todo salió bien, verás tu mensaje en WhatsApp.")
    print("Recuerda: No muevas el ratón mientras el código escribe.")
    print("--------------------------------------------------")

except Exception as e:
    print(f"Ocurrió un error: {e}")
