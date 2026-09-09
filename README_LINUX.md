# Digitador Dark Edition - Versão Linux

Esta é uma versão adaptada do Digitador Dark Edition especificamente para sistemas Linux. Ela utiliza a biblioteca `pynput` em vez de `keyboard` para garantir que o programa funcione sem a necessidade de permissões de superusuário (root/sudo) para simular a digitação.

## Diferenças da Versão Linux

- **Sem Sudo**: Não requer `sudo` para rodar.
- **Biblioteca Pynput**: Utiliza uma interface de nível de usuário para interagir com o teclado.
- **Compatibilidade**: Testado em ambientes X11 e Wayland (distribuições modernas como Ubuntu, Fedora, Mint).

## Pré-requisitos

Você precisará do Python 3 e do suporte ao Tkinter instalado no seu sistema. Em distribuições baseadas no Debian/Ubuntu, você pode instalar o Tkinter com:

```bash
sudo apt-get install python3-tk
```

## Instalação

1. Navegue até a pasta do projeto:
   ```bash
   cd darkdigitador/Dark_digitador
   ```

2. Instale a biblioteca necessária:
   ```bash
   pip install -r requirements_linux.txt
   ```

## Como Usar

1. Execute o programa:
   ```bash
   python3 digitador_linux.py
   ```

2. Cole o texto desejado na área de texto ou abra um arquivo `.txt`.
3. Clique em **"INICIAR DIGITAÇÃO AUTOMÁTICA"**.
4. Você terá **3 segundos** para clicar na janela ou campo onde o texto deve ser digitado.

## Dicas para Linux

- Se você estiver usando **Wayland** (padrão em versões recentes do Ubuntu/Fedora) e encontrar problemas, tente rodar a aplicação em uma sessão X11, embora o `pynput` tenha boa compatibilidade geral.
- Certifique-se de que o foco da janela esteja no local correto após o clique inicial.

---
Desenvolvido por Srdark1. Adaptado para Linux por Manus AI.

## Criando um Executável (App)

Para transformar o script em um arquivo executável único que você pode levar para qualquer lugar:

1. Execute o script de build:
   ```bash
   python3 build_linux.py
   ```
2. O arquivo será gerado em `dist/Digitador_Dark_Linux`.

## Adicionando ao Menu do Sistema

Para que o Digitador apareça no seu menu de aplicativos:

1. Copie o executável gerado para uma pasta permanente (ex: `/home/seu-usuario/bin/`).
2. Edite o arquivo `digitador.desktop` ajustando o caminho em `Exec=`.
3. Edite também `Icon=` para apontar para o caminho absoluto de `digitador-icon-256.png`.
4. Copie o arquivo `.desktop` para a pasta de aplicações do sistema:
   ```bash
   cp digitador.desktop ~/.local/share/applications/
   ```
