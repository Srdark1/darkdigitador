import tkinter as tk
from tkinter import filedialog, messagebox
from pynput.keyboard import Controller
import threading
import time
import os
import sys


def caminho_recurso(nome):
    """Localiza recursos tanto no código-fonte quanto no executável PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)

# Inicializa o controlador do teclado
keyboard = Controller()
parar_evento = threading.Event()

def digitar_texto():
    texto = campo_texto.get("1.0", tk.END)
    # Remove o último caractere de nova linha que o tkinter adiciona automaticamente
    if texto.endswith('\n'):
        texto = texto[:-1]
        
    for _ in range(3):
        if parar_evento.is_set():
            janela.after(0, finalizar_digitacao)
            return
        time.sleep(1)  # tempo para o usuário mudar de janela
    
    for caractere in texto:
        try:
            if parar_evento.is_set():
                janela.after(0, finalizar_digitacao)
                return
            keyboard.type(caractere)
            # Um pequeno delay para simular digitação humana e evitar bloqueios
            time.sleep(0.05)
        except Exception as e:
            print(f"Erro ao digitar caractere: {e}")

def iniciar_digitacao():
    parar_evento.clear()
    botao_comecar.config(state="disabled", text="PREPARANDO...")
    botao_parar.config(state="normal")
    threading.Thread(target=digitar_texto, daemon=True).start()

def finalizar_digitacao():
    botao_comecar.config(state="normal", text="INICIAR DIGITAÇÃO AUTOMÁTICA")
    botao_parar.config(state="disabled")

def parar_digitacao():
    parar_evento.set()

def abrir_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])
    if caminho:
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                campo_texto.delete("1.0", tk.END)
                campo_texto.insert(tk.END, conteudo)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo: {e}")

def sobre():
    messagebox.showinfo("Sobre", "Digitador Dark Edition v3.0 - Linux\nUsando pynput para compatibilidade X11/Wayland.")

# Configuração da Janela Principal
janela = tk.Tk()
janela.title("Digitador Dark Edition (Linux)")
janela.geometry("560x560")
janela.minsize(500, 500)
janela.configure(bg="#0b0b12")
janela.grid_columnconfigure(0, weight=1)
janela.grid_rowconfigure(0, weight=1)
try:
    icone = tk.PhotoImage(file=caminho_recurso("digitador-icon.png"))
    janela.iconphoto(True, icone)
except tk.TclError:
    pass

# Menu
menu_bar = tk.Menu(janela)
janela.config(menu=menu_bar)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Abrir Arquivo", command=abrir_arquivo)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=janela.quit)

menu_sobre = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Sobre", menu=menu_sobre)
menu_sobre.add_command(label="Sobre o App", command=sobre)

# Interface
conteudo_frame = tk.Frame(janela, bg="#0b0b12", highlightthickness=0, bd=0)
conteudo_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
conteudo_frame.grid_columnconfigure(0, weight=1)
conteudo_frame.grid_rowconfigure(1, weight=1)

label_instrucao = tk.Label(
    conteudo_frame,
    text="Cole o texto abaixo e clique em começar.\nVocê terá 3 segundos para focar na janela de destino.",
    bg="#0b0b12",
    fg="#f4f4fb",
    font=("Arial", 9)
)
label_instrucao.grid(row=0, column=0, pady=(0, 10))

campo_texto = tk.Text(
    conteudo_frame,
    height=12,
    width=55,
    bg="#141421",
    fg="#f4f4fb",
    insertbackground="#9b5cff",
    font=("Courier", 10)
)
campo_texto.grid(row=1, column=0, sticky="nsew", pady=10)

acoes_principais = tk.Frame(conteudo_frame, bg="#0b0b12")
acoes_principais.grid(row=2, column=0, sticky="ew", pady=10)
acoes_principais.grid_columnconfigure(0, weight=1)

botao_comecar = tk.Button(
    acoes_principais,
    text="INICIAR DIGITAÇÃO AUTOMÁTICA",
    command=iniciar_digitacao,
    bg="#9b5cff",
    fg="#fff",
    activebackground="#ad78ff",
    activeforeground="#fff",
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
botao_comecar.grid(row=0, column=0, sticky="ew", padx=(0, 8))

botao_parar = tk.Button(
    acoes_principais,
    text="■  PARAR",
    command=parar_digitacao,
    bg="#d64f6a",
    fg="#fff",
    activebackground="#ef6b82",
    activeforeground="#fff",
    state="disabled",
    font=("Arial", 10, "bold"),
    cursor="hand2",
    padx=18,
    pady=8,
)
botao_parar.grid(row=0, column=1)

janela.mainloop()
