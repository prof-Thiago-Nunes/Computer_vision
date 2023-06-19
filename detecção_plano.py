# Importa os pacotes necessários
from imutils.video import VideoStream
import imutils
import time
import cv2

# Seleciona o dicionário ArUco a ser usado
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
aruco_params = cv2.aruco.DetectorParameters_create()

# Inicializa a transmissão de vídeo e permite que o sensor da câmera aqueça
video_stream = VideoStream(src=0).start()
time.sleep(2.0)

# Loop sobre os quadros da transmissão de vídeo
while True:
    # Capta o quadro da transmissão de vídeo em paralelo e redimensiona para ter uma largura máxima de 1000 pixels
    frame = video_stream.read()
    frame = imutils.resize(frame, width=720)

    # Detecta os marcadores ArUco no quadro de entrada
    corners, ids, _ = cv2.aruco.detectMarkers(frame, dictionary, parameters=aruco_params)

    # Verifica se pelo menos um marcador ArUco foi detectado
    if len(corners) > 0:
        # Aplana a lista de IDs ArUco
        ids = ids.flatten()

        # Loop sobre os cantos ArUCo detectados
        for marker_corner, marker_id in zip(corners, ids):
            # Extrai os cantos do marcador (que são sempre retornados em ordem superior esquerda, superior direita, inferior direita e inferior esquerda)
            corners = marker_corner.reshape((4, 2))
            top_left, top_right, bottom_right, bottom_left = corners

            # Converte cada par de coordenadas (x, y) em inteiros
            top_right = (int(top_right[0]), int(top_right[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
            top_left = (int(top_left[0]), int(top_left[1]))

            # Desenha a caixa delimitadora da detecção ArUCo
            cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
            cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
            cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
            cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)

            # Calcula e desenha as coordenadas do centro (x, y) do marcador ArUco
            center_x = int((top_left[0] + bottom_right[0]) / 2.0)
            center_y = int((top_left[1] + bottom_right[1]) / 2.0)
            cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

            # Desenha o ID do marcador ArUco no quadro
            cv2.putText(frame, str(marker_id),
                        (top_left[0], top_left[1] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    # Mostra o quadro de saída
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # Se a tecla 'q' for pressionada, sai do loop
    if key == ord("q"):
        break

# Faz uma pequena limpeza
cv2.destroyAllWindows()
video_stream.stop()
