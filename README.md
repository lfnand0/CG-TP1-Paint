# CG-TP1-Paint

# Instalação
Caso esteja usando Windows, é possível rodar o programa através do arquivo main.exe presente no repositório.
Para rodar o código, siga as informações abaixo.

## Dependências
* Python 3.11.6 ou superior
* Pip:

    O script irá tentar baixar automaticamente o pip. Caso isso não seja possível, tente o seguinte:
    
    #### Linux ou MacOS:
    ``` python -m ensurepip --upgrade ```
    #### Windows:
    ``` py -m ensurepip --upgrade ```

    Caso não funcione, baixe e execute no terminal o script no link a seguir: https://bootstrap.pypa.io/get-pip.py.

* Requests:

    Após instalar o pip, execute no cmd ou terminal:
    
    ``` python -m pip install requests ```

* Tkinter:

    No Windows, o Tkinter vem baixado por padrão para as versões do Python 3.11.6 ou superior.
    Caso o código reclame da falta do tkinter ao executar, faça o seguinte:

    #### MacOS (usando brew):
    ``` brew install tkinter ```
    #### Linux (Debian):
    ``` sudo apt-get install python-tk ```
    #### Linux (Arch):
    ``` sudo pacman -S tk ```
    #### Linux (Fedora):
    ``` sudo dnf install python3-tkinter ```
    #### Linux (RHEL, CentOS, Oracle):
    ``` sudo yum install -y tkinter tk-devel ```

## Executando

No diretório contendo os arquivos, execute:
``` python main.py ```

Ou (dependendo do seu sistema operacional): 
``` python3 main.py ```


## Estrutura de Arquivos

O projeto está estruturado da seguinte forma:

```
CG-TP1-Paint/
|__ .gitignore
|__ classes.py
|__ constants.py
|__ lib.py
|__ main.exe
|__ main.py
|__ README.md
```

- `classes.py`: Contém as definições das classes utilizadas no projeto, incluindo classes descrevendo o funcionamento dos pixels, linhas, círculos e estruturas (interface para linhas e círculos).
- `constants.py`: Arquivo contendo constantes utilizado no projeto (Tamanho da janela da aplicação, tamanho dos pixels, tamanho do grid).
- `main.exe`: Executável para Windows (criado utilizando pyinstaller)
- `lib.py`: Imports e afins do projeto.
- `main.py`: Arquivo principal do projeto, contendo a criação da janela do Tkinter e chamada inicial para a classe inicializadora do projeto (classe Paint)
- `README.md`: O arquivo que você está lendo agora :)

## Funcionalidades Principais

- **Desenho de Linhas**: Linhas podem ser criadas com dois algoritmos diferentes, DDA e Bresenham. Clique nos botões "Draw Line (DDA)" ou "Draw Line (Bresenham)" e selecione dois pontos na tela para desenhar uma linha.
- **Desenho de Círculos**: Os círculos são desenhados utilizando o algoritmo de Bresenham. Clique no botão "Draw Circle (Bresenham)", selecione dois pontos na tela (o primeiro será o centro da circunferência) para desenhar um círculo.
- **Desenho de Pixels**: Clique no botão "Draw Pixel" para desenhar pontos individuais (essa opção vem selecionada por padrão ao abrir a aplicação).
- **Transformações**: Existem as opções de translação, rotação, escala e reflexão. Essas funções operam sobre todas as estruturas desenhadas na tela.
    - **Translação**: Os valores x e y digitados serão somados à cada estrutura;
    - **Rotação**: Digite um ângulo, e o x e y do valor central. As estruturas serão rotacionadas ao redor desse ponto (x, y).
    - **Escala**: As estruturas serão escaladas pelos valores x e y digitados. Para círculos, apenas o valor x será utilizado (multiplica o tamanho do raio)
    - **Reflexão**: Opções de refletir no eixo x, eixo y (ou ambos), e valores x e y do ponto que será considerado como a origem desses eixos.
- **Seleção de Cores**: Utilize o botão "Color Picker" para selecionar a cor da estrutura a ser desenhada.
- **Limpeza da Tela**: Limpa a tela.

## Classes
