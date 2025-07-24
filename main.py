import speech_recognition as sr
import socket
import json
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer

# Verifica conexão com a internet
def tem_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Modo online com Google
def modo_online():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("🟢 Assistente ONLINE. Fale algo (Ctrl + C para sair):")
        while True:
            try:
                print("\n🎤 Ouvindo...")
                audio = r.listen(source)
                texto = r.recognize_google(audio, language="pt-BR")
                print("🗣️ Você disse:", texto)
            except sr.UnknownValueError:
                print("🤔 Não entendi o que foi dito.")
            except sr.RequestError as e:
                print(f"❌ Erro com a API do Google: {e}")
                print("🔁 Alternando para modo OFFLINE...")
                modo_offline()
                break
            except KeyboardInterrupt:
                print("\n🔚 Finalizando...")
                break

# Modo offline com Vosk
def modo_offline():
    model_path = r"\\Truenas\truenas\Assitente-Virtual\modelos\vosk-model-small-pt-0.3"  # ajuste seu caminho aqui
    try:
        model = Model(model_path)
    except Exception as e:
        print(f"❌ Erro ao carregar modelo Vosk: {e}")
        return

    rec = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    print("🔵 Assistente OFFLINE. Fale algo (Ctrl + C para sair):")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    texto = result.get("text", "")
                    if texto:
                        print("🗣️ Você disse:", texto)
        except KeyboardInterrupt:
            print("\n🔚 Finalizando...")

# Chamada principal
if __name__ == "__main__":
    if tem_internet():
        modo_online()
    else:
        modo_offline()
