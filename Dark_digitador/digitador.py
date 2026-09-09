import tkinter as tk
from tkinter import filedialog, messagebox
import keyboard
import threading
import time
import os
import sys


def caminho_recurso(nome):
    """Localiza recursos tanto no código-fonte quanto no executável PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)


def digitar_texto():
    texto = campo_texto.get("1.0", tk.END)
    time.sleep(2)  # Tempo pra você clicar no lugar certo
    for caractere in texto:
        keyboard.write(caractere)
        time.sleep(0.05)


def iniciar_digitacao():
    threading.Thread(target=digitar_texto).start()


def abrir_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])
    if caminho:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            campo_texto.delete("1.0", tk.END)
            campo_texto.insert(tk.END, conteudo)


def sobre():
    messagebox.showinfo("Sobre", "Digitador Dark Edition v3.0\nDigitador real caractere por caractere!")


janela = tk.Tk()
janela.title("Digitador Dark Edition")
janela.geometry("500x400")
janela.configure(bg="#000")
try:
    icone = tk.PhotoImage(file=caminho_recurso("digitador-icon.png"))
    janela.iconphoto(True, icone)
except tk.TclError:
    pass

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

conteudo_frame = tk.Frame(janela, bg="#000", highlightthickness=0, bd=0)
conteudo_frame.pack(fill="x", pady=(10, 0))

campo_texto = tk.Text(
    conteudo_frame,
    height=12,
    width=55,
    bg="#000",
    fg="#8a2be2",  # roxo
    insertbackground="#8a2be2",
)
campo_texto.pack(pady=10)

botao_comecar = tk.Button(
    conteudo_frame,
    text="COMEÇAR A DIGITAR",
    command=iniciar_digitacao,
    bg="#222",
    fg="#fff",
    activebackground="#333",
    activeforeground="#fff",
)
botao_comecar.pack(pady=10)

janela.mainloop()
