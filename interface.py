# interface.py (VERSÃO CORRIGIDA E SIMPLIFICADA)

import tkinter as tk
from tkinter import scrolledtext, ttk
from groq import Groq
import main  # Importa nosso main.py corrigido
import threading

# ======================================================================
# !!! COLOQUE SUA CHAVE DA API GEMINI AQUI !!!
CHAVE_API_GROQ = "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"  
# ======================================================================

client = Groq(api_key=CHAVE_API_GROQ)

class AssistenteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente Virtual (Groq)")
        self.root.geometry("600x400")
        
        self.assistant_thread = None

        # --- WIDGETS DA INTERFACE ---
        self.historico = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, state="disabled")
        self.historico.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Frame para entrada de texto e botão de voz
        input_frame = ttk.Frame(root)
        input_frame.pack(padx=10, pady=(0, 10), fill="x")

        self.caixa_texto = ttk.Entry(input_frame)
        self.caixa_texto.pack(side="left", fill="x", expand=True, ipady=4)
        self.caixa_texto.bind("<Return>", self.iniciar_chat)
        
        self.btn_voz = ttk.Button(input_frame, text="🎤", command=self.toggle_assistente_voz)
        self.btn_voz.pack(side="right", padx=(5, 0))

        self.status_label = ttk.Label(root, text="Status: Inativo")
        self.status_label.pack(padx=10, pady=(0,5), anchor="w")

        # Garante que a thread pare ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def responder_ia(self, mensagem):
        """Envia a mensagem para a IA do Grok e retorna a resposta."""
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": mensagem,
                    }
                ],
                # Você pode escolher outros modelos disponíveis na Groq, como 'llama3-70b-8192'
                model="llama3-8b-8192", 
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Erro na resposta da IA (Groq): {e}"
    def iniciar_chat(self, event=None):
        """Função para enviar mensagem de texto para a IA."""
        entrada = self.caixa_texto.get().strip()
        if not entrada:
            return
        
        self.adicionar_ao_historico(f"Você: {entrada}")
        self.caixa_texto.delete(0, tk.END)
        
        resposta_ia = self.responder_ia(entrada)
        self.adicionar_ao_historico(f"Assistente: {resposta_ia}")
        
    def toggle_assistente_voz(self):
        """Inicia ou para o assistente de voz."""
        if self.assistant_thread and self.assistant_thread.is_alive():
            # Se estiver rodando, para
            main.stop_assistant()
            self.status_label.config(text="Status: Parando...")
            self.btn_voz.config(text="🎤")
        else:
            # Se não estiver rodando, inicia
            self.btn_voz.config(text="🛑")
            self.adicionar_ao_historico("--- Iniciando assistente de voz ---")
            
            # Decide qual função usar (online ou offline)
            target_function = main.start_modo_online if main.tem_internet() else main.start_modo_offline
            
            # Cria e inicia a thread do assistente
            self.assistant_thread = threading.Thread(
                target=target_function,
                args=(self.atualizar_status, self.processar_resultado_voz),
                daemon=True
            )
            self.assistant_thread.start()

    def processar_resultado_voz(self, texto_reconhecido):
        """Função chamada pela thread de voz com o texto reconhecido."""
        self.adicionar_ao_historico(f"Você (voz): {texto_reconhecido}")
        resposta_ia = self.responder_ia(texto_reconhecido)
        self.adicionar_ao_historico(f"Assistente: {resposta_ia}")

    def adicionar_ao_historico(self, texto):
        """Adiciona uma mensagem na caixa de histórico."""
        self.historico.config(state="normal")
        self.historico.insert(tk.END, texto + "\n\n")
        self.historico.see(tk.END) # Rola para o final
        self.historico.config(state="disabled")

    def atualizar_status(self, texto_status):
        """Atualiza a label de status (chamado pela thread)."""
        self.status_label.config(text=f"Status: {texto_status}")
        # Se o assistente parou, reseta o botão
        if "parado" in texto_status.lower():
            self.btn_voz.config(text="🎤")

    def on_closing(self):
        """Função para garantir que tudo pare ao fechar a janela."""
        if self.assistant_thread and self.assistant_thread.is_alive():
            main.stop_assistant()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistenteApp(root)
    root.mainloop()