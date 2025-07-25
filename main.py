import speech_recognition as sr
import socket
import json
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import threading

# Esta variável de evento será usada para parar a thread de forma segura
stop_thread = threading.Event()

# Verifica conexão com a internet
def tem_internet():
    """Tenta conectar a um servidor externo para verificar a conexão."""
    try:
        # Tenta se conectar ao DNS do Google na porta 53 (padrão para DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Conexão com a internet detectada.")
        return True
    except OSError:
        print("❌ Sem conexão com a internet.")
        return False

# Modo online com Google
def start_modo_online(status_callback, result_callback):
    """
    Inicia o assistente no modo ONLINE, comunicando-se com a interface.
    - status_callback: Função da interface para atualizar o status (ex: "Ouvindo...").
    - result_callback: Função da interface para mostrar o texto reconhecido.
    """
    stop_thread.clear()  # Reseta o sinal de parada
    r = sr.Recognizer()

    status_callback("🟢 Online | Pronto")
    while not stop_thread.is_set():
        try:
            with sr.Microphone() as source:
                status_callback("🟢 Assistente ONLINE. Fale algo (Ctrl + C para sair):")
                 # Ajusta o listen com um timeout para não bloquear para sempre
                audio = r.listen(source, timeout=5, phrase_time_limit=10)

            status_callback("🔍 Reconhecendo...")
            texto = r.recognize_google(audio, language="pt-BR")
            result_callback(texto) # Envia apenas o texto puro para a interface
        
        except sr.WaitTimeoutError:
            # Se não houver fala, o loop continua sem erro
            continue
        except sr.UnknownValueError:
            # Ignora se não entender
            continue
        except sr.RequestError as e:
            status_callback(f"❌ Erro de API: {e}")
            break # Para o loop se a API falhar
    status_callback("🔌 Assistente parado.")
    
# Modo offline com Vosk
def start_modo_offline(status_callback, result_callback):
    """Inicia o assistente no modo OFFLINE, comunicando-se com a interface."""
    stop_thread.clear()
    # ======================================================================
    # !!! MUITO IMPORTANTE: AJUSTE O CAMINHO DO SEU MODELO VOSK AQUI !!!
    model_path = ("adicionar-proprio-caminho")  # ajuste seu caminho aqui
    try:
        model = Model(model_path)
    except Exception as e:
        status_callback(f"❌ Erro ao carregar modelo Vosk: {e}")
        return

    rec = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def audio_callback(indata, frames, time, status):
        q.put(bytes(indata))

    status_callback("🔵 Offline | Pronto")
    with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                           channels=1, callback=audio_callback):
     while not stop_thread.is_set():
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                texto = result.get("text", "")
                if texto:
                    result_callback(texto) # Envia o texto puro para a interface
    
    status_callback("🔌 Assistente parado.")

def stop_assistant():
    """Função chamada pela interface para sinalizar a parada da thread."""
    stop_thread.set()
