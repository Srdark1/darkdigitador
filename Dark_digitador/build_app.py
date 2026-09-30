from pathlib import Path
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
ENTRYPOINT = ROOT / "digitador.py"
ICON = ROOT / "digitador-icon.ico"
PNG_ICON = ROOT / "digitador-icon.png"
REQUIREMENTS = ROOT / "requirements.txt"
DIST = ROOT / "dist"
BUILD = ROOT / "build"


def executar(comando):
    print("$", " ".join(map(str, comando)))
    subprocess.check_call(comando, cwd=ROOT)


def instalar_dependencias():
    """Instala as dependências fixadas do aplicativo e do PyInstaller."""
    executar([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)])
    executar([sys.executable, "-m", "pip", "install", "pyinstaller==6.3.0"])


def criar_executavel():
    """Gera o executável Windows a partir do código atual."""
    if not ENTRYPOINT.exists():
        raise FileNotFoundError(f"Arquivo principal não encontrado: {ENTRYPOINT}")

    DIST.mkdir(exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    nome = "Digitador_Dark_Edition"

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

    if ICON.exists():
        comando.append(f"--icon={ICON}")
    if PNG_ICON.exists():
        # os.pathsep funciona tanto no Windows (;) quanto no Linux (:).
        comando.append(f"--add-data={PNG_ICON}{os.pathsep}.")

    comando.append(str(ENTRYPOINT))
    executar(comando)

    executavel = DIST / (f"{nome}.exe" if os.name == "nt" else nome)
    if not executavel.exists():
        raise RuntimeError(f"O build terminou sem gerar: {executavel}")

    print(f"\nExecutável criado com sucesso: {executavel}")
    print(f"Tamanho: {executavel.stat().st_size:,} bytes")


if __name__ == "__main__":
    try:
        instalar_dependencias()
        criar_executavel()
    except (FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as erro:
        print(f"\nERRO no build: {erro}", file=sys.stderr)
        raise SystemExit(1)
