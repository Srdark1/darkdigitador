import os
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

import keyboard


# Paleta visual do Digitador Dark Edition
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
STOP = "#d64f6a"
STOP_HOVER = "#ef6b82"

parar_evento = threading.Event()
pause_evento = threading.Event()
pausa_inicial_cancelada = threading.Event()
rodando = False
texto_atual = ""
arquivo_atual = None
modo_atual = "avancado"
retomada_em_andamento = False
atalho_pausa = None


def caminho_recurso(nome):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)


def atualizar_contador(_event=None):
    conteudo = campo_texto.get("1.0", "end-1c")
    caracteres = len(conteudo)
    palavras = len(conteudo.split())
    contador.config(text=f"{caracteres:,} caracteres • {palavras:,} palavras")
    atualizar_estimativa()


def atualizar_estimativa():
    texto = campo_texto.get("1.0", "end-1c")
    try:
        intervalo = max(0, float(intervalo_var.get())) / 1000
        atraso = max(0, float(atraso_var.get()))
        pausa_linha = max(0, float(pausa_linha_var.get())) / 1000
    except ValueError:
        return
    linhas = texto.count("\n") if preservar_var.get() else 0
    segundos = atraso + (len(texto) * intervalo) + (linhas * pausa_linha)
    exec_duracao.config(text=formatar_tempo(segundos) if texto else "—")
    velocidade = int(1 / intervalo) if intervalo > 0 else 0
    velocidade_label.config(text=f"Velocidade estimada: {velocidade:,} caracteres/s" if velocidade else "Velocidade máxima")


def formatar_tempo(segundos):
    segundos = max(0, int(round(segundos)))
    return f"{segundos // 60:02d}:{segundos % 60:02d}"


def definir_status(texto, cor=MUTED):
    janela.after(0, lambda: status.config(text=texto, fg=cor))


def atualizar_execucao(enviados, total, decorrido=None, destino=None):
    def atualizar():
        exec_caracteres.config(text=f"{enviados:,} / {total:,}")
        if decorrido is not None:
            exec_tempo.config(text=formatar_tempo(decorrido))
            restante = max(0, total - enviados) * max(0.001, float(intervalo_var.get()) / 1000)
            exec_restante.config(text=formatar_tempo(restante))
        if destino:
            exec_destino.config(text=destino)
        progresso.set((enviados / total) if total else 0)
        progresso_barra.coords("fill", 0, 0, progresso.get() * progresso_barra.winfo_width(), 6)
        progresso_label.config(text=f"{enviados:,} de {total:,} caracteres enviados • {int((enviados / total) * 100) if total else 0}% concluído")
    janela.after(0, atualizar)


def finalizar_digitacao(mensagem="Pronto para digitar", cor=MUTED):
    global rodando, retomada_em_andamento
    rodando = False
    retomada_em_andamento = False
    campo_texto.config(state="normal")
    botao_comecar.config(state="normal", text="▶  COMEÇAR A DIGITAR")
    botao_pausar.config(state="disabled", text="Ⅱ  PAUSAR")
    botao_parar.config(state="disabled")
    abrir_botao.config(state="normal")
    apagar_botao.config(state="normal")
    for widget in controles:
        widget.config(state="normal")
    definir_status(mensagem, cor)
    janela.after(0, lambda: modo_label.config(text="Modelo avançado  /  Editor pronto", fg=MUTED))


def aguardar_com_cancelamento(segundos):
    fim = time.time() + segundos
    while time.time() < fim:
        if parar_evento.is_set():
            return False
        time.sleep(min(0.05, fim - time.time()))
    return True


def digitar_texto(texto, intervalo, atraso, pausa_linha, preservar):
    total = len(texto)
    inicio = time.time()
    definir_status("Selecione a janela de destino agora", WARNING)
    janela.after(0, lambda: modo_label.config(text="Modelo avançado  /  Contagem regressiva", fg=WARNING))

    for segundos in range(int(atraso), 0, -1):
        if parar_evento.is_set():
            janela.after(0, finalizar_digitacao, "Início cancelado", WARNING)
            return
        definir_status(f"Iniciando em {segundos} segundo{'s' if segundos != 1 else ''}", WARNING)
        janela.after(0, lambda s=segundos: contagem_label.config(text=str(s)))
        if not aguardar_com_cancelamento(1):
            janela.after(0, finalizar_digitacao, "Início cancelado", WARNING)
            return

    janela.after(0, lambda: contagem_label.config(text="⌨"))
    definir_status("Digite mantendo a janela de destino em foco", ACCENT)
    janela.after(0, lambda: modo_label.config(text="Modelo avançado  /  Em execução", fg=SUCCESS))

    enviados = 0
    for indice, caractere in enumerate(texto):
        while pause_evento.is_set() and not parar_evento.is_set():
            definir_status("Digitação pausada", WARNING)
            time.sleep(0.1)
        if parar_evento.is_set():
            janela.after(0, finalizar_digitacao, "Digitação interrompida", WARNING)
            return
        try:
            keyboard.write(caractere)
        except Exception as erro:
            janela.after(0, finalizar_digitacao, f"Erro ao digitar: {erro}", STOP)
            return
        enviados = indice + 1
        decorrido = time.time() - inicio
        atualizar_execucao(enviados, total, decorrido, "Janela selecionada")
        if preservar and caractere == "\n" and pausa_linha > 0:
            if not aguardar_com_cancelamento(pausa_linha):
                janela.after(0, finalizar_digitacao, "Digitação interrompida", WARNING)
                return
        elif intervalo > 0 and not aguardar_com_cancelamento(intervalo):
            janela.after(0, finalizar_digitacao, "Digitação interrompida", WARNING)
            return

    atualizar_execucao(total, total, time.time() - inicio, "Concluído")
    janela.after(0, finalizar_digitacao, "Digitação concluída", SUCCESS)


def iniciar_digitacao():
    global rodando, texto_atual
    texto_atual = campo_texto.get("1.0", "end-1c")
    if not texto_atual.strip():
        definir_status("Digite ou carregue um texto antes de começar", WARNING)
        campo_texto.focus_set()
        return
    try:
        intervalo = max(0, float(intervalo_var.get())) / 1000
        atraso = max(0, float(atraso_var.get()))
        pausa_linha = max(0, float(pausa_linha_var.get())) / 1000
    except ValueError:
        definir_status("Confira os valores dos ajustes de digitação", WARNING)
        return

    rodando = True
    parar_evento.clear()
    pause_evento.clear()
    campo_texto.config(state="disabled")
    botao_comecar.config(state="disabled", text="⌛  PREPARANDO...")
    botao_pausar.config(state="normal", text="Ⅱ  PAUSAR")
    botao_parar.config(state="normal")
    abrir_botao.config(state="disabled")
    apagar_botao.config(state="disabled")
    for widget in controles:
        widget.config(state="disabled")
    exec_caracteres.config(text=f"0 / {len(texto_atual):,}")
    exec_tempo.config(text="00:00")
    exec_restante.config(text="—")
    progresso.set(0)
    progresso_barra.coords("fill", 0, 0, 0, 6)
    progresso_label.config(text=f"0 de {len(texto_atual):,} caracteres enviados • 0% concluído")
    threading.Thread(target=digitar_texto, args=(texto_atual, intervalo, atraso, pausa_linha, preservar_var.get()), daemon=True).start()


def alternar_pausa():
    global retomada_em_andamento
    if not rodando:
        return
    if pause_evento.is_set():
        if not retomada_em_andamento:
            try:
                segundos = max(0, int(float(tempo_retomada_var.get())))
            except ValueError:
                segundos = 3
            retomada_em_andamento = True
            iniciar_retomada(segundos)
    else:
        pause_evento.set()
        botao_pausar.config(text="▶  RETOMAR")
        contagem_label.config(text="Ⅱ")
        definir_status("Digitação pausada", WARNING)


def iniciar_retomada(segundos):
    """Faz a contagem regressiva antes de liberar a thread de digitação."""
    global retomada_em_andamento
    if not rodando or not pause_evento.is_set():
        retomada_em_andamento = False
        return
    if segundos <= 0:
        pause_evento.clear()
        retomada_em_andamento = False
        botao_pausar.config(state="normal", text="Ⅱ  PAUSAR")
        contagem_label.config(text="⌨")
        definir_status("Digitação retomada", ACCENT)
        return
    botao_pausar.config(state="disabled", text=f"RETOMANDO {segundos}...")
    contagem_label.config(text=str(segundos))
    definir_status(f"Retomando em {segundos} segundo{'s' if segundos != 1 else ''}", WARNING)
    janela.after(1000, iniciar_retomada, segundos - 1)


def parar_digitacao():
    if rodando:
        parar_evento.set()
        pause_evento.clear()
        definir_status("Interrompendo a digitação...", WARNING)


def abrir_arquivo():
    global arquivo_atual
    caminho = filedialog.askopenfilename(title="Abrir arquivo de texto", filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
    if caminho:
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                campo_texto.config(state="normal")
                campo_texto.delete("1.0", tk.END)
                campo_texto.insert("1.0", arquivo.read())
                arquivo_atual = os.path.basename(caminho)
                arquivo_nome.config(text=arquivo_atual, fg=SUCCESS)
                atualizar_contador()
                definir_status("Texto carregado. Tudo pronto para começar.", SUCCESS)
        except (OSError, UnicodeDecodeError) as erro:
            messagebox.showerror("Não foi possível abrir", str(erro))


def limpar_texto():
    campo_texto.config(state="normal")
    campo_texto.delete("1.0", tk.END)
    arquivo_nome.config(text="Nenhum arquivo", fg=MUTED)
    atualizar_contador()
    definir_status("Área de texto limpa", MUTED)
    campo_texto.focus_set()


def sobre():
    messagebox.showinfo("Sobre o Digitador Dark Edition", "Digitador Dark Edition v4.0\n\nDigitação automática com controles avançados, progresso, pausa e interrupção.")


def fechar_janela():
    parar_evento.set()
    if atalho_pausa is not None:
        try:
            keyboard.remove_hotkey(atalho_pausa)
        except (KeyError, OSError):
            pass
    janela.destroy()


def alternar_modo(novo_modo):
    """Alterna entre o fluxo simples e o painel de ajustes avançados."""
    global modo_atual
    if rodando:
        definir_status("Aguarde a digitação terminar para trocar o modo", WARNING)
        return
    modo_atual = novo_modo
    if novo_modo == "simples":
        # O modo simples mantém a digitação funcionando com valores seguros,
        # mas deixa a tela livre dos ajustes técnicos.
        intervalo_var.set("50")
        atraso_var.set("5")
        pausa_linha_var.set("0")
        tempo_retomada_var.set("3")
        preservar_var.set(True)
        ajustes.pack_forget()
        modo_simples.config(bg=SURFACE_ALT, fg=TEXT, font=("Segoe UI", 9, "bold"))
        modo_avancado.config(bg=SURFACE, fg=MUTED, font=("Segoe UI", 9))
        modo_label.config(text="Modelo simples  /  Editor pronto", fg=MUTED)
    else:
        ajustes.pack(fill="x", pady=(0, 18), before=execucao)
        modo_simples.config(bg=SURFACE, fg=MUTED, font=("Segoe UI", 9))
        modo_avancado.config(bg=SURFACE_ALT, fg=TEXT, font=("Segoe UI", 9, "bold"))
        modo_label.config(text="Modelo avançado  /  Editor pronto", fg=MUTED)
    atualizar_estimativa()


janela = tk.Tk()
janela.title("Digitador Dark Edition")
janela.geometry("1180x780")
janela.minsize(900, 680)
janela.configure(bg=BG)
janela.grid_columnconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)
janela.protocol("WM_DELETE_WINDOW", fechar_janela)
try:
    icone = tk.PhotoImage(file=caminho_recurso("digitador-icon.png"))
    janela.iconphoto(True, icone)
except tk.TclError:
    pass

menu_bar = tk.Menu(janela, bg=SURFACE, fg=TEXT, activebackground=ACCENT, activeforeground=TEXT, borderwidth=0, relief="flat")
janela.config(menu=menu_bar)
menu_arquivo = tk.Menu(menu_bar, tearoff=0, bg=SURFACE, fg=TEXT, activebackground=ACCENT, activeforeground=TEXT, borderwidth=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Abrir arquivo...", command=abrir_arquivo)
menu_arquivo.add_command(label="Limpar texto", command=limpar_texto)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=fechar_janela)
menu_sobre = tk.Menu(menu_bar, tearoff=0, bg=SURFACE, fg=TEXT, activebackground=ACCENT, activeforeground=TEXT, borderwidth=0)
menu_bar.add_cascade(label="Sobre", menu=menu_sobre)
menu_sobre.add_command(label="Sobre o app", command=sobre)

# Cabeçalho
cabecalho = tk.Frame(janela, bg=BG)
cabecalho.grid(row=0, column=0, sticky="ew", padx=46, pady=(28, 18))
tk.Label(cabecalho, text="DIGITADOR", bg=BG, fg=ACCENT, font=("Segoe UI", 23, "bold")).pack(side="left")
tk.Label(cabecalho, text=" Dark Edition", bg=BG, fg=TEXT, font=("Segoe UI", 23, "bold")).pack(side="left")
tk.Label(cabecalho, text="Automatize sua digitação com precisão e simplicidade.", bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(side="left", padx=(24, 0), pady=(8, 0))
modo = tk.Frame(cabecalho, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
modo.pack(side="right")
modo_simples = tk.Button(modo, text="Simples", command=lambda: alternar_modo("simples"), bg=SURFACE, fg=MUTED, activebackground=SURFACE_ALT, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 9), padx=20, pady=9)
modo_simples.pack(side="left")
modo_avancado = tk.Button(modo, text="Avançado", command=lambda: alternar_modo("avancado"), bg=SURFACE_ALT, fg=TEXT, activebackground=SURFACE_ALT, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 9, "bold"), padx=20, pady=9)
modo_avancado.pack(side="left")

# Área central com editor e painel lateral
principal = tk.Frame(janela, bg=BG)
principal.grid(row=1, column=0, sticky="nsew", padx=46)
principal.grid_columnconfigure(0, weight=3)
principal.grid_columnconfigure(1, weight=1)
principal.grid_rowconfigure(0, weight=1)

cartao = tk.Frame(principal, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
cartao.grid(row=0, column=0, sticky="nsew", padx=(0, 22))
cartao.grid_columnconfigure(0, weight=1)
cartao.grid_rowconfigure(1, weight=1)
barra = tk.Frame(cartao, bg=SURFACE)
barra.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 12))
tk.Label(barra, text="▧  Seu texto", bg=SURFACE, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
contador = tk.Label(barra, text="0 caracteres • 0 palavras", bg=SURFACE, fg=MUTED, font=("Segoe UI", 9))
contador.pack(side="right")
editor_frame = tk.Frame(cartao, bg="#080810", highlightbackground=BORDER, highlightthickness=1)
editor_frame.grid(row=1, column=0, sticky="nsew", padx=22, pady=(0, 12))
editor_frame.grid_columnconfigure(0, weight=1)
editor_frame.grid_rowconfigure(0, weight=1)
campo_texto = tk.Text(editor_frame, bg="#080810", fg=TEXT, insertbackground=ACCENT, selectbackground=ACCENT, selectforeground=TEXT, relief="flat", borderwidth=0, wrap="word", undo=True, font=("Cascadia Mono", 11), padx=16, pady=14)
campo_texto.grid(row=0, column=0, sticky="nsew")
scroll = tk.Scrollbar(editor_frame, command=campo_texto.yview, bg="#080810", troughcolor="#080810", activebackground=ACCENT, relief="flat", width=10)
scroll.grid(row=0, column=1, sticky="ns")
campo_texto.config(yscrollcommand=scroll.set)
campo_texto.bind("<KeyRelease>", atualizar_contador)
rodape_cartao = tk.Frame(cartao, bg=SURFACE)
rodape_cartao.grid(row=2, column=0, sticky="ew", padx=22, pady=(0, 18))
abrir_botao = tk.Button(rodape_cartao, text="▱  ABRIR ARQUIVO", command=abrir_arquivo, bg=SURFACE_ALT, fg=TEXT, activebackground=ACCENT, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 9, "bold"), padx=12, pady=7)
abrir_botao.pack(side="left")
apagar_botao = tk.Button(rodape_cartao, text="▱  APAGAR TEXTO", command=limpar_texto, bg=SURFACE_ALT, fg=TEXT, activebackground=ACCENT, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 9, "bold"), padx=12, pady=7)
apagar_botao.pack(side="left", padx=(8, 0))
arquivo_nome = tk.Label(rodape_cartao, text="Nenhum arquivo", bg=SURFACE, fg=MUTED, font=("Segoe UI", 9))
arquivo_nome.pack(side="right")

# Painel de ajustes e execução
lateral = tk.Frame(principal, bg=BG)
lateral.grid(row=0, column=1, sticky="nsew")
lateral.grid_columnconfigure(0, weight=1)

def criar_cartao(titulo):
    frame = tk.Frame(lateral, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
    frame.pack(fill="x", pady=(0, 18))
    tk.Label(frame, text=titulo, bg=SURFACE, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(16, 12))
    return frame

ajustes = criar_cartao("☷  Ajustes de digitação")
intervalo_var = tk.StringVar(value="50")
atraso_var = tk.StringVar(value="5")
pausa_linha_var = tk.StringVar(value="0")
tempo_retomada_var = tk.StringVar(value="3")
preservar_var = tk.BooleanVar(value=True)
controles = []

def campo_ajuste(parent, texto, variavel, unidade):
    linha = tk.Frame(parent, bg=SURFACE)
    linha.pack(fill="x", padx=18, pady=5)
    tk.Label(linha, text=texto, bg=SURFACE, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")
    entrada = tk.Entry(linha, textvariable=variavel, width=7, justify="right", bg=SURFACE_ALT, fg=TEXT, insertbackground=ACCENT, relief="flat", font=("Cascadia Mono", 10))
    entrada.pack(side="right", padx=(8, 4), ipady=5)
    tk.Label(linha, text=unidade, bg=SURFACE, fg=MUTED, font=("Segoe UI", 8)).pack(side="right")
    entrada.bind("<KeyRelease>", lambda _e: atualizar_estimativa())
    controles.append(entrada)
    return entrada

campo_ajuste(ajustes, "Intervalo por tecla", intervalo_var, "ms")
campo_ajuste(ajustes, "Atraso inicial", atraso_var, "s")
campo_ajuste(ajustes, "Pausa entre linhas", pausa_linha_var, "ms")
campo_ajuste(ajustes, "Tempo para retomar", tempo_retomada_var, "s")
linha_preservar = tk.Frame(ajustes, bg=SURFACE)
linha_preservar.pack(fill="x", padx=18, pady=(8, 4))
tk.Label(linha_preservar, text="Preservar quebras de linha", bg=SURFACE, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")
tk.Checkbutton(linha_preservar, variable=preservar_var, bg=SURFACE, activebackground=SURFACE, selectcolor=ACCENT, command=atualizar_estimativa).pack(side="right")
velocidade_label = tk.Label(ajustes, text="Velocidade estimada: 25 caracteres/s", bg=SURFACE, fg=MUTED, font=("Segoe UI", 8))
velocidade_label.pack(anchor="w", padx=18, pady=(5, 16))

execucao = criar_cartao("〽  Execução")
for titulo, valor in [("Caracteres enviados", "0 / 0"), ("Tempo decorrido", "00:00"), ("Tempo restante", "—"), ("Destino", "Não selecionado")]:
    linha = tk.Frame(execucao, bg=SURFACE)
    linha.pack(fill="x", padx=18, pady=4)
    tk.Label(linha, text=titulo, bg=SURFACE, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")
    label = tk.Label(linha, text=valor, bg=SURFACE, fg=TEXT, font=("Segoe UI", 9, "bold"))
    label.pack(side="right")
    if titulo == "Caracteres enviados": exec_caracteres = label
    elif titulo == "Tempo decorrido": exec_tempo = label
    elif titulo == "Tempo restante": exec_restante = label
    else: exec_destino = label
exec_duracao = tk.Label(execucao, text="—", bg=SURFACE, fg=MUTED, font=("Segoe UI", 8))
exec_duracao.pack_forget()

# Rodapé de status, progresso e ações
rodape = tk.Frame(janela, bg=BG)
rodape.grid(row=2, column=0, sticky="ew", padx=46, pady=(12, 20))
rodape.grid_columnconfigure(0, weight=1)
status_frame = tk.Frame(rodape, bg=BG)
status_frame.grid(row=0, column=0, sticky="w")
status = tk.Label(status_frame, text="Pronto para digitar", bg=BG, fg=SUCCESS, font=("Segoe UI", 10, "bold"))
status.pack(anchor="w")
modo_label = tk.Label(status_frame, text="Modelo avançado  /  Editor pronto", bg=BG, fg=MUTED, font=("Segoe UI", 8))
modo_label.pack(anchor="w", pady=(3, 0))
acoes = tk.Frame(rodape, bg=BG)
acoes.grid(row=0, column=1, sticky="e")
contagem_label = tk.Label(acoes, text="", bg=BG, fg=WARNING, font=("Segoe UI", 18, "bold"))
contagem_label.pack(side="left", padx=(0, 18))
botao_comecar = tk.Button(acoes, text="▶  COMEÇAR A DIGITAR", command=iniciar_digitacao, bg=ACCENT, fg=TEXT, activebackground=ACCENT_HOVER, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 10, "bold"), padx=22, pady=12)
botao_comecar.pack(side="left")
botao_pausar = tk.Button(acoes, text="Ⅱ  PAUSAR", command=alternar_pausa, state="disabled", bg=ACCENT, fg=TEXT, activebackground=ACCENT_HOVER, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 10, "bold"), padx=18, pady=12)
botao_pausar.pack(side="left", padx=(8, 0))
botao_parar = tk.Button(acoes, text="□  APARAR", command=parar_digitacao, state="disabled", bg=SURFACE_ALT, fg=STOP_HOVER, activebackground=STOP, activeforeground=TEXT, relief="flat", borderwidth=0, cursor="hand2", font=("Segoe UI", 10, "bold"), padx=18, pady=12)
botao_parar.pack(side="left", padx=(8, 0))
progresso = tk.DoubleVar(value=0)
progresso_barra = tk.Canvas(rodape, height=6, bg=SURFACE_ALT, highlightthickness=0)
progresso_barra.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(14, 4))
progresso_barra.create_rectangle(0, 0, 0, 6, fill=ACCENT, outline="", tags="fill")
progresso_label = tk.Label(rodape, text="0 de 0 caracteres enviados • 0% concluído", bg=BG, fg=MUTED, font=("Segoe UI", 8))
progresso_label.grid(row=2, column=0, sticky="w")
tk.Label(rodape, text="Mantenha a janela de destino em foco.   •   F8 pausa/retoma   •   Esc interrompe", bg=BG, fg=MUTED, font=("Segoe UI", 8)).grid(row=2, column=1, sticky="e")
janela.bind("<Escape>", lambda _e: parar_digitacao())
try:
    atalho_pausa = keyboard.add_hotkey("f8", lambda: janela.after(0, alternar_pausa))
except (ImportError, OSError, RuntimeError):
    atalho_pausa = None

campo_texto.focus_set()
atualizar_contador()
janela.mainloop()
