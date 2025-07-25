# interface_estilizada.py

import tkinter as tk
from tkinter import ttk, scrolledtext 
from PIL import Image, ImageTk  # Importa a biblioteca de imagens
from groq import Groq
import main  # Nosso backend continua o mesmo
import threading

# ======================================================================
# !!! COLOQUE SUA CHAVE DA API GROQ AQUI !!!
CHAVE_API_GROQ = "SUA-API-KEY-AQUI"
# ======================================================================

client = Groq(api_key=CHAVE_API_GROQ)

# --- Definição de Cores e Fontes ---
COR_FUNDO_LARANJA = "#F39C12"
COR_FUNDO_MENU = "#2C3E50"
COR_TEXTO_MENU = "#F39C12"
COR_FUNDO_BARRA_INFERIOR = "#1C2833"
COR_FUNDO_CHAT = "#34495E" # Cor para o fundo do chat
COR_TEXTO_CHAT = "#FFFFFF" # Cor para o texto no chat
FONTE_PRINCIPAL = ("Segoe UI", 12)
FONTE_TITULO = ("Segoe UI", 16, "bold")
FONTE_CHAT = ("Segoe UI", 10)


class AssistenteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Artemis - Assistente I.A")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.root.configure(bg=COR_FUNDO_LARANJA)

        self.assistant_thread = None

        # --- ESTRUTURA PRINCIPAL ---
        menu_frame = tk.Frame(root, bg=COR_FUNDO_MENU, width=300) # Aumentei um pouco a largura do menu
        menu_frame.pack(side="right", fill="y")
        menu_frame.pack_propagate(False)

        content_frame = tk.Frame(root, bg=COR_FUNDO_LARANJA)
        content_frame.pack(side="left", fill="both", expand=True)

        bottom_bar = tk.Frame(root, bg=COR_FUNDO_BARRA_INFERIOR, height=20)
        bottom_bar.pack(side="bottom", fill="x")

        self.criar_menu(menu_frame)
        self.criar_conteudo(content_frame)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def criar_menu(self, parent_frame):
        """Cria todos os widgets dentro do menu lateral."""
        tk.Label(parent_frame, text="Menu", font=FONTE_TITULO, bg=COR_FUNDO_MENU, fg="white").pack(pady=20)

        # Botões do Menu
        botoes_menu = {
            "Iniciar Reconhecimento de Voz": self.toggle_assistente_voz,
            "Ligar Camera": self.acao_placeholder,
            "Ações": self.acao_placeholder,
            "Verificar o Perimetro": self.acao_placeholder,
        }
        for texto_btn, comando_btn in botoes_menu.items():
            btn = tk.Button(parent_frame, text=texto_btn, font=FONTE_PRINCIPAL, bg=COR_FUNDO_MENU, fg=COR_TEXTO_MENU, command=comando_btn, relief="flat", anchor="w", padx=20)
            btn.pack(fill="x", pady=5)
        
        # Linha separadora
        ttk.Separator(parent_frame, orient='horizontal').pack(fill='x', pady=10, padx=20)

        # <<< MUDANÇA 1: Adicionando o quadro de mensagens (Chat Box) >>>
        self.chat_box = scrolledtext.ScrolledText(
            parent_frame,
            wrap=tk.WORD,
            state="disabled", # Começa desabilitado para o usuário não digitar
            bg=COR_FUNDO_CHAT,
            fg=COR_TEXTO_CHAT,
            font=FONTE_CHAT,
            relief="flat",
            padx=10,
            pady=10
        )
        # O chat_box ocupa o espaço restante, expandindo
        self.chat_box.pack(pady=10, padx=20, fill="both", expand=True)

        # Status Label no final do menu
        self.status_label = tk.Label(parent_frame, text="Status: Inativo", bg=COR_FUNDO_MENU, fg="white", anchor="w", padx=20)
        self.status_label.pack(side="bottom", fill="x", pady=10)

    def criar_conteudo(self, parent_frame):
        """Cria os widgets da área de conteúdo principal."""
        header_frame = tk.Frame(parent_frame, bg=COR_FUNDO_LARANJA)
        header_frame.pack(fill="x", padx=20, pady=20)

        try:
            pil_image = Image.open("avatar_a.jng").resize((60, 60), Image.Resampling.LANCZOS)
            self.avatar_image = ImageTk.PhotoImage(pil_image)
            tk.Label(header_frame, image=self.avatar_image, bg=COR_FUNDO_LARANJA).pack(side="left")
        except FileNotFoundError:
            tk.Label(header_frame, text=" A ", font=("Arial", 24, "bold"), bg="white", fg=COR_FUNDO_LARANJA).pack(side="left", padx=10)

        title_text_frame = tk.Frame(header_frame, bg=COR_FUNDO_LARANJA)
        title_text_frame.pack(side="left", padx=15)
        
        tk.Label(title_text_frame, text="Artemis", font=("Segoe UI", 20, "bold"), bg=COR_FUNDO_LARANJA, fg="white").pack(anchor="w")
        tk.Label(title_text_frame, text="Assistente I.A", font=FONTE_PRINCIPAL, bg=COR_FUNDO_LARANJA, fg="white").pack(anchor="w")

        character_container = tk.Frame(parent_frame, bg="#D35400")
        character_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tk.Label(character_container, text="Área Reservada para Personagem 3D", font=FONTE_TITULO, bg="#D35400", fg="white").pack(expand=True)

    def acao_placeholder(self):
        print(f"Botão clicado! Esta função ainda precisa ser implementada.")

    def responder_ia(self, mensagem):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": mensagem}],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Erro na resposta da IA (Groq): {e}"

    def toggle_assistente_voz(self):
        if self.assistant_thread and self.assistant_thread.is_alive():
            main.stop_assistant()
            self.atualizar_status("Parando...")
        else:
            self.atualizar_status("Iniciando...")
            target_function = main.start_modo_online if main.tem_internet() else main.start_modo_offline
            self.assistant_thread = threading.Thread(
                target=target_function,
                args=(self.atualizar_status, self.processar_resultado_voz),
                daemon=True
            )
            self.assistant_thread.start()

    def processar_resultado_voz(self, texto_reconhecido):
        self.root.after(0, self.exibir_conversa, "Você", texto_reconhecido)
        threading.Thread(target=self.obter_resposta_async, args=(texto_reconhecido,), daemon=True).start()

    def obter_resposta_async(self, entrada):
        resposta_ia = self.responder_ia(entrada)
        self.root.after(0, self.exibir_conversa, "Artemis", resposta_ia)

    # <<< MUDANÇA 2: Atualizando a função para escrever no Chat Box >>>
    def exibir_conversa(self, autor, texto):
        """Insere a mensagem formatada na caixa de chat."""
        if not texto: return # Não exibe nada se o texto estiver vazio

        self.chat_box.config(state="normal") # Habilita para poder escrever

        # Formata a mensagem com o autor em negrito
        if autor == "Artemis":
            self.chat_box.tag_configure("artemis_tag", font=(FONTE_CHAT[0], FONTE_CHAT[1], "bold"), foreground=COR_TEXTO_MENU)
            self.chat_box.insert(tk.END, f"{autor}:\n", "artemis_tag")
        else:
            self.chat_box.tag_configure("user_tag", font=(FONTE_CHAT[0], FONTE_CHAT[1], "bold"))
            self.chat_box.insert(tk.END, f"{autor}:\n", "user_tag")

        self.chat_box.insert(tk.END, f"{texto}\n\n")
        self.chat_box.see(tk.END) # Rola para a mensagem mais recente
        self.chat_box.config(state="disabled") # Desabilita novamente

    def atualizar_status(self, texto_status):
        self.status_label.config(text=f"Status: {texto_status}")

    def on_closing(self):
        if self.assistant_thread and self.assistant_thread.is_alive():
            main.stop_assistant()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistenteApp(root)
    root.mainloop()
