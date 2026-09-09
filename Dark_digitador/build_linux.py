import subprocess
import sys
import os

def instalar_dependencias():
    """Instala as dependências necessárias para o build"""
    print("Instalando dependências de build...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "pynput"])
        print("Dependências instaladas com sucesso!")
    except Exception as e:
        print(f"Erro ao instalar dependências: {e}")

def criar_executavel():
    """Cria o executável do digitador para Linux"""
    print("Criando executável do Digitador Dark Edition (Linux)...")
    
    # Comando para criar o executável
    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Digitador_Dark_Linux",
        "--add-data=digitador-icon.png:.",
        "digitador_linux.py"
    ]
    
    try:
        subprocess.check_call(comando)
        print("\n✅ Executável Linux criado com sucesso!")
        print("📁 Arquivo: dist/Digitador_Dark_Linux")
        print("🎉 Você pode rodar o arquivo na pasta dist diretamente!")
        
        # Tornar o arquivo executável (comando linux)
        if os.path.exists("dist/Digitador_Dark_Linux"):
            os.chmod("dist/Digitador_Dark_Linux", 0o755)
            print("🔑 Permissões de execução aplicadas.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")

if __name__ == "__main__":
    instalar_dependencias()
    criar_executavel()
