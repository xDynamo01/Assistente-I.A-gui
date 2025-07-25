#Dowload do modelo de linguagem pt-BR
import zipfile
import os
import requests
from vosk import Model

url = "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip"
zip_path = "vosk_pt.zip"
model_dir = "modelos/vosk-model-small-pt-0.3"

# Baixar o modelo
if not os.path.exists(model_dir):
    print("Baixando modelo de voz em português...")
    r = requests.get(url, stream=True)
    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)

    print("Extraindo modelo...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("modelos")

    os.remove(zip_path)

# Carregar o modelo
model = Model(model_dir)
 
