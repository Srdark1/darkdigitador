import subprocess
import sys
import os

def instalar_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("PyInstaller já está instalado!")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller instalado com sucesso!")

def criar_executavel():
    """Cria o executável do digitador"""
    print("Criando executável do Digitador Dark Edition...")
    import sys
    
    # Caminho absoluto da imagem (lida com espaços no nome)
    caminho_imagem = os.path.abspath("Igris22 (1).jpg")

    # Comando para criar o executável usando o Python atual
    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # Cria um único arquivo executável
        "--windowed",  # Não mostra console ao executar
        "--name=Digitador_Dark_Edition",  # Nome do executável
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",  # Ícone se existir
        # Empacota a imagem de fundo (Windows usa ";" como separador de destino)
        (f"--add-data={caminho_imagem};." if os.path.exists(caminho_imagem) else ""),
        "digitador.py"
    ]
    
    # Remove o ícone do comando se não existir
    comando = [item for item in comando if item]
    
    try:
        subprocess.check_call(comando)
        print("\n✅ Executável criado com sucesso!")
        print("📁 Arquivo: dist/Digitador_Dark_Edition.exe")
        print("🎉 Você pode copiar o .exe para qualquer lugar e usar!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")

if __name__ == "__main__":
    instalar_pyinstaller()
    criar_executavel() 