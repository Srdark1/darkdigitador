import tkinter as tk
from tkinter import filedialog, messagebox
from pynput.keyboard import Controller
import threading
import time

# Inicializa o controlador do teclado
keyboard = Controller()

def digitar_texto():
    texto = campo_texto.get("1.0", tk.END)
    # Remove o último caractere de nova linha que o tkinter adiciona automaticamente
    if texto.endswith('\n'):
        texto = texto[:-1]
        
    time.sleep(3)  # 3 segundos para o usuário mudar de janela
    
    for caractere in texto:
        try:
            keyboard.type(caractere)
            # Um pequeno delay para simular digitação humana e evitar bloqueios
            time.sleep(0.05)
        except Exception as e:
            print(f"Erro ao digitar caractere: {e}")

def iniciar_digitacao():
    threading.Thread(target=digitar_texto, daemon=True).start()

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
janela.geometry("500x450")
janela.configure(bg="#000")

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
conteudo_frame = tk.Frame(janela, bg="#000", highlightthickness=0, bd=0)
conteudo_frame.pack(fill="both", expand=True, padx=20, pady=10)

label_instrucao = tk.Label(
    conteudo_frame, 
    text="Cole o texto abaixo e clique em começar.\nVocê terá 3 segundos para focar na janela de destino.",
    bg="#000", 
    fg="#fff",
    font=("Arial", 9)
)
label_instrucao.pack(pady=(0, 10))

campo_texto = tk.Text(
    conteudo_frame,
    height=12,
    width=55,
    bg="#111",
    fg="#8a2be2",  # Roxo Dark
    insertbackground="#8a2be2",
    font=("Courier", 10)
)
campo_texto.pack(fill="both", expand=True, pady=10)

botao_comecar = tk.Button(
    conteudo_frame,
    text="INICIAR DIGITAÇÃO AUTOMÁTICA",
    command=iniciar_digitacao,
    bg="#222",
    fg="#fff",
    activebackground="#8a2be2",
    activeforeground="#000",
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
botao_comecar.pack(pady=10, fill="x")

janela.mainloop()
