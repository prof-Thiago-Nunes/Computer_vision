import numpy as np
import cv2
import glob


"""Critério de terminação: ou após 30 iterações ou se os cantos forem encontrados 
com a precisão desejada."""

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Preparando os pontos do objeto (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
# As dimensões (7,10) são baseadas no números de cantos em seu tabuleiro de xadrez.

objp = np.zeros((7*10, 3), np.float32)
objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2)

# Cria listas para armazenar os pontos do objeto e os pontos de todas as imagens.
objpoints = []  # Pontos 3d no espaço do mundo real.
imgpoints = []  # Pontos 2d no plano da imagem.

# Lê todas as imagens do diretório atual que começam com 'chessboard'
images = glob.glob('chessboard/*.JPG')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Encontra os cantos do tabuleiro de xadrez
    ret, corners = cv2.findChessboardCorners(gray, (10, 7), None)

    """Se os cantos forem encontrados, forem encontrados, 
    adicione os pontos do objeto e os pontos do objeto e os 
    pontos da imagem (após refinar os cantos)"""

    if ret == True:
        objpoints.append(objp)


        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)


        # Desenha e exibe os cantos
        img = cv2.drawChessboardCorners(img, (10, 7), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Calibra a câmera e retorna a matriz da câmera, coeficientes de distorção, vetores de rotação e vetores de translação
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


# Imprime os valores da calibração
print("Matriz da câmera: ")
print(mtx)

print("Coeficiente de distorção: ")
print(dist)

print("Vetores de rotação: ")
print(rvecs)

print("Vetores de translação: ")
print(tvecs)

# Salva os valores de calibração em um arquivo
np.savez('calib.npz', mtx = mtx, dist = dist, rvecs = rvecs, tvecs = tvecs)

