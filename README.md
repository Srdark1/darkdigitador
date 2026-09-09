# Digitador Dark Edition

## Descrição do Projeto

O Digitador Dark Edition é uma aplicação desktop desenvolvida em Python utilizando a biblioteca `tkinter` para a interface gráfica. Sua principal função é automatizar a digitação de texto, permitindo que o usuário insira um conteúdo manualmente ou carregue-o de um arquivo `.txt`. O programa então simula a digitação desse texto caractere por caractere, com um pequeno atraso entre cada um, ideal para situações que exigem a inserção de grandes volumes de texto de forma controlada.

## Funcionalidades

*   **Interface Gráfica Intuitiva**: Desenvolvida com `tkinter`, oferece uma experiência de usuário simples e direta.
*   **Digitação Automatizada**: Simula a digitação de texto caractere por caractere, com um atraso configurável.
*   **Carregamento de Arquivos**: Permite carregar conteúdo de arquivos `.txt` para digitação.
*   **Executável Standalone**: Pode ser compilado em um executável único para Windows, facilitando a distribuição e o uso sem a necessidade de instalar o Python ou suas dependências.

## Pré-requisitos

Para executar o projeto a partir do código-fonte, você precisará ter o Python instalado em sua máquina. As dependências específicas do projeto podem ser instaladas via `pip`.

*   Python 3.x
*   `keyboard`
*   `pyinstaller` (necessário apenas para construir o executável)

## Instalação

Siga os passos abaixo para configurar e executar o projeto:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Srdark1/darkdigitador.git
    cd darkdigitador/Dark_digitador
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Usar

1.  **Execute a aplicação:**
    ```bash
    python digitador.py
    ```

2.  **Interface da Aplicação:**
    *   Uma janela com um campo de texto será exibida.
    *   Você pode digitar o texto diretamente no campo ou usar a opção `Arquivo > Abrir Arquivo` para carregar um arquivo `.txt`.
    *   Clique no botão "COMEÇAR A DIGITAR".
    *   Após clicar, você terá 2 segundos para posicionar o cursor no local onde deseja que o texto seja digitado (por exemplo, em um editor de texto, navegador, etc.).
    *   O programa começará a digitar o texto automaticamente.

## Construindo o Executável (Windows)

O projeto inclui um script `build_app.py` para criar um executável Windows usando `PyInstaller`.

1.  **Navegue até a pasta `Dark_digitador`:**
    ```bash
    cd darkdigitador/Dark_digitador
    ```

2.  **Execute o script de build:**
    ```bash
    python build_app.py
    ```

    Este script irá:
    *   Verificar e instalar o `PyInstaller` se necessário.
    *   Compilar o `digitador.py` em um executável `Digitador_Dark_Edition.exe` na pasta `dist`.
    *   O executável será `onefile` (arquivo único) e `windowed` (sem console).
    *   O ícone `digitador-icon.ico` será aplicado ao executável e `digitador-icon.png` será incluído para a janela do app.
    *   O arquivo opcional `Igris22 (1).jpg` também será incluído como recurso visual, se estiver presente.

## Sobre

**Digitador Dark Edition v3.0**

Um digitador que simula a digitação real caractere por caractere.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` (se disponível) para mais detalhes.
