import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Microphone with name '{name}' found for `Microphone(device_index={index})`")