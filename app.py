# Importando as bibliotecas necessárias
import cv2
import numpy as np

# Carregando os dois vídeos do projeto
cap_webcam = cv2.VideoCapture('video\webcam.mp4')
cap_praia = cv2.VideoCapture('video\praia.mp4')

# Loop da integração dos vídeos
while True:
    # Leitura Frame a Frame dos vídeos
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    # Finalizando o loop da leitura dos frames do vídeo
    if not ret_webcam or not ret_praia:
        break

    # Definindo os limites da cor de fundo verde para criar uma máscara
    lower_green = np.array([0, 115, 0], dtype = np.uint8)
    upper_green = np.array([100, 255, 100], dtype = np.uint8)

    # Criando uma máscara com os pixels que estão dentro dos limites superiores e inferiores
    # Limite inferior (lower_green) e limite superior (upper_green)
    mask = cv2.inRange(frame_webcam, lower_green, upper_green )

     # Usa a máscara para extrair os pixels da praia que correspondem ao fundo verde da webcam.
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    # Utilizando a máscara criada para extrair os pixels do vídeo praia.mp4 
    # Os quais são correspondentes ao fundo verde do vídeo webcam.mp4
    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    # Invertendo a máscara para obter os pixels que não estão na faixa da cor verde
    mask_inv = np.invert(mask)

    # Utiliza a máscara invertida para obter os pixels da webcam que não são verdes
    webcam_foreground = cv2.bitwise_and(frame_webcam, frame_webcam, mask = mask_inv)

    # Verificando o resultado da transformação do background
    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    cv2.imshow("Resultado", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap_webcam.release()
cap_praia.release()
cv2.destroyAllWindows()
