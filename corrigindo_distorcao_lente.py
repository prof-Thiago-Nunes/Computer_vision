# Importando os pacotes necessários
import numpy as np
import cv2
import argparse
import matplotlib.pyplot as plt

def corrigir_lente(image_path, calibration_file):
    # Carregando os parâmetros de calibração
    with np.load(calibration_file) as X:
        mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]

    # Carregando a imagem
    img = cv2.imread("imagens\gopro.jpg")

    # Crrigindo imagem
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
                            
    # Corrigindo 
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    return img, dst

def plot_images(img, dst):
    # Plota a imagem original e a imagem desdistorcida lado a lado
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
    plt.title('Undistorted Image')

    plt.show()

def main():
    parser = argparse.ArgumentParser(description = "Corrigindo a distorção da lente")
    parser.add_argument("-i", "--image_path", type=str, required=True, help="Caminho para a imagem de entrada")
    args = parser.parse_args()

    # Carregando a distorção da imagem
    img, dst = corrigir_lente(args.image_path, "calib.npz")

    # Plotando as imagens
    plot_images(img, dst)

if __name__ == "__main__":
    main()





