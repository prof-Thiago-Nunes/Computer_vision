# Importando as bibliotecas necessárias
import cv2
import numpy as np

# Definindo o tamanho do quadro de saída
largura = 640
altura = 480

# Definindo o nome e o codec do arquivo de saída
nome_arquivo_saida = 'video_saida.mp4'
codec_saida = cv2.VideoWriter_fourcc(*'mp4v')

# Criando o objeto VideoWriter para gravar o vídeo de saída
video_saida = cv2.VideoWriter(nome_arquivo_saida, codec_saida, 30.0, (largura, altura))

# Carregando os dois vídeos do projeto
cap_webcam = cv2.VideoCapture('video/webcam.mp4')
cap_praia = cv2.VideoCapture('video/praia.mp4')

# Loop da integração dos vídeos
while True:
    # Leitura Frame a Frame dos vídeos
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    # Finalizando o loop da leitura dos frames do vídeo
    if not ret_webcam or not ret_praia:
        break

    # Redimensionando os quadros para o tamanho desejado
    frame_webcam = cv2.resize(frame_webcam, (largura, altura))
    frame_praia = cv2.resize(frame_praia, (largura, altura))

    # Definindo os limites da cor de fundo verde para criar uma máscara
    lower_green = np.array([0, 115, 0], dtype=np.uint8)
    upper_green = np.array([100, 255, 100], dtype=np.uint8)

    # Criando uma máscara com os pixels que estão dentro dos limites superiores e inferiores
    mask = cv2.inRange(frame_webcam, lower_green, upper_green)

    # Usa a máscara para extrair os pixels da praia que correspondem ao fundo verde da webcam.
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    # Invertendo a máscara para obter os pixels que não estão na faixa da cor verde
    mask_inv = np.invert(mask)

    # Utiliza a máscara invertida para obter os pixels da webcam que não são verdes
    webcam_foreground = cv2.bitwise_and(frame_webcam, frame_webcam, mask=mask_inv)

    # Verificando o resultado da transformação do background
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    cv2.imshow("Resultado", result)

    # Gravando o quadro no vídeo de saída
    video_saida.write(result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberando recursos e fechando objetos
cap_webcam.release()
cap_praia.release()
video_saida.release()
cv2.destroyAllWindows()