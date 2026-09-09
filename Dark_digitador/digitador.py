import os
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

import keyboard


# Paleta visual do aplicativo
BG = "#0b0b12"
SURFACE = "#141421"
SURFACE_ALT = "#1b1b2a"
BORDER = "#2b2b3d"
TEXT = "#f4f4fb"
MUTED = "#9a9aac"
ACCENT = "#9b5cff"
ACCENT_HOVER = "#ad78ff"
SUCCESS = "#55d6a7"
WARNING = "#ffc857"


def caminho_recurso(nome):
    """Localiza recursos tanto no código-fonte quanto no executável PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)


def atualizar_contador(_event=None):
    conteudo = campo_texto.get("1.0", "end-1c")
    caracteres = len(conteudo)
    palavras = len(conteudo.split())
    contador.config(text=f"{caracteres:,} caracteres  •  {palavras:,} palavras")


def definir_status(texto, cor=MUTED):
    janela.after(0, lambda: status.config(text=texto, fg=cor))


def finalizar_digitacao():
    botao_comecar.config(state="normal", text="▶  COMEÇAR A DIGITAR")
    definir_status("Pronto para digitar", MUTED)


def digitar_texto(texto):
    definir_status("Mude para a janela de destino...", WARNING)
    for segundos in (2, 1):
        definir_status(f"Começando em {segundos} segundo{'s' if segundos != 1 else ''}...", WARNING)
        time.sleep(1)

    definir_status("Digitando seu texto...", ACCENT)
    for caractere in texto:
        keyboard.write(caractere)
        time.sleep(0.05)

    janela.after(0, finalizar_digitacao)


def iniciar_digitacao():
    texto = campo_texto.get("1.0", "end-1c")
    if not texto.strip():
        definir_status("Digite ou carregue um texto antes de começar", WARNING)
        campo_texto.focus_set()
        return

    botao_comecar.config(state="disabled", text="⌛  PREPARANDO...")
    threading.Thread(target=digitar_texto, args=(texto,), daemon=True).start()


def abrir_arquivo():
    caminho = filedialog.askopenfilename(
        title="Abrir arquivo de texto",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
    )
    if caminho:
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                campo_texto.delete("1.0", tk.END)
                campo_texto.insert("1.0", arquivo.read())
                atualizar_contador()
                definir_status(f"Arquivo carregado: {os.path.basename(caminho)}", SUCCESS)
        except (OSError, UnicodeDecodeError) as erro:
            messagebox.showerror("Não foi possível abrir", str(erro))


def limpar_texto():
    campo_texto.delete("1.0", tk.END)
    atualizar_contador()
    definir_status("Área de texto limpa", MUTED)
    campo_texto.focus_set()


def sobre():
    messagebox.showinfo(
        "Sobre o Digitador Dark Edition",
        "Digitador Dark Edition v3.0\n\nDigite textos automaticamente, caractere por caractere.",
    )


janela = tk.Tk()
janela.title("Digitador Dark Edition")
janela.geometry("760x560")
janela.minsize(620, 460)
janela.configure(bg=BG)
try:
    icone = tk.PhotoImage(file=caminho_recurso("digitador-icon.png"))
    janela.iconphoto(True, icone)
except tk.TclError:
    pass

# Menu discreto, com as mesmas ações do app original
menu_bar = tk.Menu(janela, bg=SURFACE, fg=TEXT, activebackground=ACCENT, activeforeground=TEXT,
                   borderwidth=0, relief="flat")
janela.config(menu=menu_bar)
menu_arquivo = tk.Menu(menu_bar, tearoff=0, bg=SURFACE, fg=TEXT, activebackground=ACCENT,
                       activeforeground=TEXT, borderwidth=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Abrir arquivo...", command=abrir_arquivo)
menu_arquivo.add_command(label="Limpar texto", command=limpar_texto)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=janela.destroy)
menu_sobre = tk.Menu(menu_bar, tearoff=0, bg=SURFACE, fg=TEXT, activebackground=ACCENT,
                     activeforeground=TEXT, borderwidth=0)
menu_bar.add_cascade(label="Sobre", menu=menu_sobre)
menu_sobre.add_command(label="Sobre o app", command=sobre)

# Cabeçalho
cabecalho = tk.Frame(janela, bg=BG)
cabecalho.pack(fill="x", padx=34, pady=(28, 18))
tk.Label(cabecalho, text="DIGITADOR", bg=BG, fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(anchor="w")
tk.Label(cabecalho, text="Dark Edition", bg=BG, fg=TEXT, font=("Segoe UI", 26, "bold")).pack(anchor="w", pady=(2, 0))
tk.Label(cabecalho, text="Automatize sua digitação com precisão e simplicidade.", bg=BG, fg=MUTED,
         font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

# Cartão principal
cartao = tk.Frame(janela, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
cartao.pack(fill="both", expand=True, padx=34, pady=(0, 18))
barra = tk.Frame(cartao, bg=SURFACE)
barra.pack(fill="x", padx=18, pady=(16, 10))
tk.Label(barra, text="Seu texto", bg=SURFACE, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
contador = tk.Label(barra, text="0 caracteres  •  0 palavras", bg=SURFACE, fg=MUTED, font=("Segoe UI", 9))
contador.pack(side="right")

editor_frame = tk.Frame(cartao, bg=SURFACE_ALT, highlightbackground=BORDER, highlightthickness=1)
editor_frame.pack(fill="both", expand=True, padx=18, pady=(0, 14))
campo_texto = tk.Text(editor_frame, bg=SURFACE_ALT, fg=TEXT, insertbackground=ACCENT,
                      selectbackground=ACCENT, selectforeground=TEXT, relief="flat", borderwidth=0,
                      wrap="word", undo=True, font=("Cascadia Mono", 11), padx=14, pady=12,
                      highlightthickness=0)
campo_texto.pack(side="left", fill="both", expand=True)
scroll = tk.Scrollbar(editor_frame, command=campo_texto.yview, bg=SURFACE_ALT, troughcolor=SURFACE_ALT,
                      activebackground=ACCENT, relief="flat", width=10)
scroll.pack(side="right", fill="y")
campo_texto.config(yscrollcommand=scroll.set)
campo_texto.bind("<KeyRelease>", atualizar_contador)

rodape_cartao = tk.Frame(cartao, bg=SURFACE)
rodape_cartao.pack(fill="x", padx=18, pady=(0, 16))
status = tk.Label(rodape_cartao, text="Pronto para digitar", bg=SURFACE, fg=MUTED,
                  font=("Segoe UI", 9))
status.pack(side="left")
tk.Button(rodape_cartao, text="Limpar", command=limpar_texto, bg=SURFACE, fg=MUTED,
          activebackground=SURFACE_ALT, activeforeground=TEXT, relief="flat", borderwidth=0,
          cursor="hand2", font=("Segoe UI", 9)).pack(side="right")

botao_comecar = tk.Button(janela, text="▶  COMEÇAR A DIGITAR", command=iniciar_digitacao,
                          bg=ACCENT, fg=TEXT, activebackground=ACCENT_HOVER, activeforeground=TEXT,
                          disabledforeground="#6e6382", relief="flat", borderwidth=0, cursor="hand2",
                          font=("Segoe UI", 11, "bold"), pady=12)
botao_comecar.pack(fill="x", padx=34, pady=(0, 10))
tk.Label(janela, text="Você terá 2 segundos para selecionar a janela de destino.", bg=BG, fg=MUTED,
         font=("Segoe UI", 9)).pack(pady=(0, 20))

campo_texto.focus_set()
janela.mainloop()
