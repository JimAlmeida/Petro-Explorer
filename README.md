## **Petro-Explorer** - Como instalar

 1. Primeiramente é preciso baixar o interpretador Python. A versão utilizada é a versão 3.9.0 64 bits para Windows. [Clique aqui para baixar](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe)
 2. Clique em *Install Now* e certifique-se de que a caixa "Add Python 3.9 to PATH" está marcada.
![Tela Instalação 1](https://imgur.com/ha94pBK.png)
 3. Aguarde o final da instalação e feche o prompt quando chegar à esta tela:![Tela Instalação 2](https://imgur.com/tFESv7S.png)
 4. Abra o prompt de comando (CMD) e teste se a instalação Python ocorreu com sucesso digitando "python". Se você ver essa tela, tudo ocorreu bem. Para sair, do interpretador digite "exit()".![Tela Instalação 3](https://imgur.com/7Aaqq3Q.png)
 5. Digite a seguinte linha de comando no CMD: 
 `python -m pip install numpy scipy pandas requests ipython nbformat psutil plotly openpyxl xlrd PySide2`
 Esse comando serve para instalar as bibliotecas utilizadas pelo programa.
![Tela Instalação 4](https://imgur.com/zTS8Wcl.png)
 6. Faça o download deste repositório para o seu Desktop. Uma possível maneira é por realizar o download direto do GitHub (Download ZIP), como na imagem:
![Tela Instalação 5](https://imgur.com/zLWVvSw.png)
7. Extraia os conteúdos do arquivo .zip para sua pasta de preferência.
8. Finalmente, é necessário criar o arquivo .bat necessário para inicializar o programa, abra o Notepad e escreva as seguintes linhas de texto:

> cd "[CAMINHO PARA A PASTA]\source" && START /B pythonw MainWindow.py

Um exemplo do que esse arquivo é para cada computador em específico, está na imagem abaixo:
![Tela Instalação 6](https://imgur.com/5XWu61j.png)
Depois que o texto for digitado, é necessário salvar o arquivo na extensão *.bat* na pasta Source do programa.
![Tela Instalação 7](https://imgur.com/UD76Cqn.png)

8. Para iniciar o programa é só clicar sobre o arquivo *.bat* ou se preferir, crie um atalho para o arquivo na sua área de trabalho. Para criar o atalho, siga os seguintes passos:
	- Com o botão direto do mouse sobre o local onde você quer o atalho, clique em Novo, e depois em Atalho.
	- Selecione o caminho para o arquivo .bat para onde o atalho irá apontar.
	![Tela 8](https://imgur.com/KnDi2av.png)
	- Forneça um nome para o atalho.                                  
	![Tela 9](https://imgur.com/2B0YigQ.png)
	- Por razões estéticas, altere o ícone do atalho.             
	![Tela 10](https://imgur.com/Rsh1Nqm.png)
	- Selecione o ícone que está na pasta ../source/icons                   
	![Tela 11](https://imgur.com/jSNxcJx.png)
	- Seu atalho ficará assim:                                   
	![Tela 12](https://imgur.com/4eGnK0S.png)
	- Clique no atalho para iniciar o programa:                             
	![Tela 13](https://imgur.com/nFh0H60.png)
**Parabéns, você chegou ao final da instalação!**

Você também pode assistir um mini-tutorial para realizar sua primeira análise com o conjunto de dados contido neste repositório. Acesse o link: https://youtu.be/DEoA1BOFzmo

