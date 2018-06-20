# Projeto final de IPI

## Alunos:
   - Kálley Wilkerson - 170038050
   - Danilo Inácio -


#### Observações
O programa assume que todas as imagens que serão usadas
estão na pasta Imagens, portanto, antes de utilizar o
programa para alguma imagem de seu próprio banco de dados
lembre-se de colocá-la na pasta Imagens.

Não existe uma pasta separada para os processos de simulação
de impressão.

Este programa foi só testado em sistemas operacionais Unix



## Módulos necessários
Observe que os módulos a frente são muito importantes, sem
eles instalados muito provavelmente o programa não irá
funcionar.

OpenCV     - (versão 3.4.1) diversas funções, única versão testada

PyWavelets - utlizada para usar a função da transformada de
             Wavelet

Numpy      - utilizada em situações variadas

sys        - utilizada para as flags no módulo principal

glob       - padrão do Python



## Como executar
Para executar o programa de maneira simples basta executar no
terminal:

>>> python3 main.py

E siga os passos que o programa passará. Na hora de
digitar o nome da imagem digite o nome junto com a extensão,
por exemplo, "gato5.png" e não "gato5" e nem "Imagens/gato5.png".

Além disso, caso queira que o programa plote os resultados
intermediários basta fazer:

>>> python3 main.py -p

Ou mais, se quiser que o programa execute para todas as imagens
na pasta Imagens, basta fazer:

>>> python3 main.py --all

E você também pode combinar essas duas opções



## Pastas
Imagens      - Onde estão as imagens utilizadas, por favor procure
               usar somente formatos mais conhecidos como .png ou
	       .jpg. Recomendamos muito que seja apenas png.

Texturizadas - Onde estão as imagens texturizadas produzidas,
               tanto imagens com simulação quanto imagens sem
	       simulação serão guardadas aqui.

Resultados   - Como é de se imaginar, esta pasta conterá os resultados
               da resuperação de cores obtidos.