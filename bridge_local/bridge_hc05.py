import serial
import requests
import time

# 1. Configuración del Bluetooth
# Reemplaza 'COM7' por el puerto de tu computadora donde está el HC-05
try:
    puerto_serial = serial.Serial('COM7', 9600, timeout=1)
    print("✅ Conectado exitosamente al HC-05 en el puerto COM7")
except Exception as e:
    print(f"❌ Error al conectar al Bluetooth: {e}")
    puerto_serial = None

# 2. Configuración del Servidor
# Por ahora usamos localhost, cuando tengas tu IP pública la cambiaremos aquí
URL_SERVIDOR = "http://localhost:5000/api/log"

print("🚀 Esperando movimientos del robot...")

while puerto_serial:
    if puerto_serial.in_waiting > 0:
        # Leer línea enviada por el robot (ej: "Adelante", "Obstáculo Detectado")
        linea = puerto_serial.readline().decode('utf-8').strip()
        
        if linea:
            print(f"🤖 Robot dice: {linea}")
            
            # Enviar el dato al Backend
            payload = {
                "accion": linea,
                "detalles": "Evento enviado vía Bluetooth HC-05"
            }
            
            try:
                res = requests.post(URL_SERVIDOR, json=payload)
                if res.status_code == 201:
                    print("📡 Evento sincronizado con la nube exitosamente.")
            except:
                print("⚠️ Error: El servidor no está respondiendo.")
    
    time.sleep(0.1)