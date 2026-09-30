from pathlib import Path
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
ENTRYPOINT = ROOT / "digitador_linux.py"
PNG_ICON = ROOT / "digitador-icon.png"
REQUIREMENTS = ROOT / "requirements_linux.txt"
DIST = ROOT / "dist"


def executar(comando):
    print("$", " ".join(map(str, comando)))
    subprocess.check_call(comando, cwd=ROOT)


def instalar_dependencias():
    """Instala as dependências fixadas da versão Linux e do PyInstaller."""
    executar([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)])
    executar([sys.executable, "-m", "pip", "install", "pyinstaller==6.3.0"])


def criar_executavel():
    """Gera o executável Linux a partir do código atual."""
    if not ENTRYPOINT.exists():
        raise FileNotFoundError(f"Arquivo principal não encontrado: {ENTRYPOINT}")

    nome = "Digitador_Dark_Linux"
    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        f"--name={nome}",
    ]
    if PNG_ICON.exists():
        comando.append(f"--add-data={PNG_ICON}{os.pathsep}.")
    comando.append(str(ENTRYPOINT))

    executar(comando)

    executavel = DIST / nome
    if not executavel.exists():
        raise RuntimeError(f"O build terminou sem gerar: {executavel}")
    executavel.chmod(executavel.stat().st_mode | 0o111)

    print(f"\nExecutável Linux criado com sucesso: {executavel}")
    print(f"Tamanho: {executavel.stat().st_size:,} bytes")


if __name__ == "__main__":
    try:
        instalar_dependencias()
        criar_executavel()
    except (FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as erro:
        print(f"\nERRO no build: {erro}", file=sys.stderr)
        raise SystemExit(1)
