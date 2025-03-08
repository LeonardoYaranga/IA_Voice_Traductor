# -*- coding: utf-8 -*-
import speech_recognition as sr
import time

def test_microphone(device_index):
    r = sr.Recognizer()
    try:
        print(f"\nProbando dispositivo: {sr.Microphone.list_microphone_names()[device_index]} (index={device_index})")
        with sr.Microphone(device_index=device_index) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Habla ahora (tienes 3 segundos)...")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
        
        # Intentar reconocer el audio
        try:
            texto = r.recognize_google(audio, language='es-ES')
            print(f"Éxito: Se detectó: '{texto}'")
            return True
        except sr.UnknownValueError:
            print("No se entendió el audio (puede que no haya sonido o el micrófono no funcione).")
            return False
        except sr.RequestError as e:
            print(f"Error al conectar con el servicio de reconocimiento: {e}")
            return False
    except ValueError as e:
        print(f"Error: Dispositivo no válido o no disponible: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def main():
    print("Listando todos los dispositivos de audio disponibles:")
    dispositivos = sr.Microphone.list_microphone_names()
    for index, name in enumerate(dispositivos):
        print(f"Índice {index}: {name}")

    print("\nProbando cada dispositivo automáticamente...")
    print("Asegúrate de hablar claro cada vez que se indique 'Habla ahora'.")
    
    # Filtrar dispositivos que probablemente no sean micrófonos
    posibles_micrófonos = [
        i for i, name in enumerate(dispositivos) 
        if "microphone" in name.lower() or "mic" in name.lower() or "input" in name.lower()
    ]
    
    if not posibles_micrófonos:
        print("No se encontraron dispositivos que parezcan micrófonos. Probando todos...")
        posibles_micrófonos = range(len(dispositivos))

    micrófonos_funcionales = []
    for index in posibles_micrófonos:
        if test_microphone(index):
            micrófonos_funcionales.append(index)
        time.sleep(1)  

    print("\nResumen:")
    if micrófonos_funcionales:
        print("Micrófonos que detectaron audio:")
        for index in micrófonos_funcionales:
            print(f"Índice {index}: {dispositivos[index]}")
    else:
        print("Ningún micrófono detectó audio. Verifica tu hardware o configuración.")

if __name__ == "__main__":
    main()