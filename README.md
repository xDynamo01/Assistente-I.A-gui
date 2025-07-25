Artemis - Assistente Virtual com IA

https://imgur.com/gallery/artemis-i-wyWyN3o

Artemis é um assistente virtual de desktop desenvolvido em Python, com uma interface gráfica moderna e responsiva, projetado para interagir com o usuário através de comandos de voz. Ele utiliza tecnologias de reconhecimento de voz online e offline e se conecta à API ultrarrápida da Groq para fornecer respostas inteligentes e contextuais através do modelo Llama 3.
A interface foi construída para ser modular e está preparada para a integração de um personagem 3D animado, tornando a experiência do usuário mais imersiva e pessoal.

✨ Características Principais
Reconhecimento de Voz Híbrido: Alterna automaticamente entre:
Modo Online: Utiliza a API do Google Speech Recognition para alta precisão quando conectado à internet.
Modo Offline: Utiliza o modelo Vosk para garantir funcionalidade mesmo sem conexão com a internet.
Inteligência Artificial de Ponta: Integrado com a API da Groq para respostas quase instantâneas do modelo de linguagem Llama 3.
Interface Gráfica Moderna: Construída com Tkinter, com um design limpo, responsivo e preparado para futuras expansões.
Pronto para Animação 3D: A estrutura da interface já possui um container dedicado para a renderização de um personagem 3D em tempo real com bibliotecas como Pyglet.
Visualização de Conversa: Um painel de chat integrado ao menu exibe o diálogo entre o usuário e a Artemis.
Código Modular: Lógica de backend (main.py) e frontend (interface_estilizada.py) separadas para facilitar a manutenção e o desenvolvimento.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3
Interface Gráfica (GUI):
Tkinter: Biblioteca padrão do Python para criação de interfaces.
Pillow (PIL): Para manipulação e exibição de imagens.
Reconhecimento de Voz:
SpeechRecognition: Para integração com a API do Google.
Vosk: Para reconhecimento de fala offline.
sounddevice: Para capturar áudio do microfone para o Vosk.
Inteligência Artificial:
groq: Cliente oficial da API da Groq para acesso ao Llama 3 e outros modelos.
Animação 3D (Estrutura Preparada):
Pyglet: Para renderização de gráficos e animações 3D em tempo real.

🚀 Configuração e Instalação
Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

1. Clone o Repositório
Generated bash
git clone https://github.com/xDynamo01/Assistente-I.A-gui.git
cd Assistente-I.A-gui
Use code with caution.
Bash
2. Crie um Ambiente Virtual (Recomendado)
Isso mantém as dependências do projeto isoladas.
Generated bash
# Para Windows
python -m venv venv
venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
Use code with caution.
Bash

3. Instale as Dependências
Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:
Generated txt
# requirements.txt
Pillow==10.4.0
SpeechRecognition==3.10.4
sounddevice==0.5.0
vosk==0.3.45
groq==0.9.0
pyglet==2.0.15
numpy==1.26.4
Use code with caution.
Txt
Depois, instale todas de uma vez com o comando:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash

4. Baixe o Modelo de Linguagem Vosk (Offline) # recomendado utilizar o dowload.py.
Para o reconhecimento de voz offline funcionar, você precisa baixar um modelo em português.
Vá para a página de modelos do Vosk.
Baixe um modelo para Português (o vosk-model-small-pt-0.3 é uma boa opção leve).
Descompacte o arquivo .zip em uma pasta dentro do seu projeto (ex: ./modelos/).
Abra o arquivo main.py e atualize o caminho para o modelo na linha indicada:
Generated python
# Em main.py
# !!! MUITO IMPORTANTE: AJUSTE O CAMINHO DO SEU MODELO VOSK AQUI !!!
model_path = r"caminho/completo/para/sua/pasta/vosk-model-small-pt-0.3"
Use code with caution.
Python
5. Configure sua Chave de API da Groq
Obtenha sua chave de API gratuita no Groq Console.
Abra o arquivo interface_estilizada.py e insira sua chave na variável CHAVE_API_GROQ:
Generated python
# Em interface_estilizada.py
# !!! COLOQUE SUA CHAVE DA API GROQ AQUI !!!
CHAVE_API_GROQ = "SUA_CHAVE_API_GROQ_AQUI"
Use code with caution.
Python
▶️ Como Utilizar
Após concluir a instalação e configuração, execute o arquivo da interface a partir do seu terminal:
Generated bash
python interface_estilizada.py
Use code with caution.
Bash
A interface da Artemis será aberta. Clique no botão "Iniciar Reconhecimento de Voz" no menu e comece a falar. A transcrição da sua fala e a resposta da IA aparecerão no quadro de mensagens.
📈 Próximos Passos (Roadmap)
Implementar a renderização do personagem 3D animado com Pyglet.
Adicionar animações de "lip-sync" (sincronia labial) para o personagem reagir à fala da IA.
Ativar as funcionalidades dos outros botões do menu ("Ligar Câmera", "Ações", etc.).
Melhorar a gestão do contexto da conversa para que a IA se lembre de interações passadas.
Adicionar um campo de texto para permitir interação via teclado, além da voz.
📄 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
