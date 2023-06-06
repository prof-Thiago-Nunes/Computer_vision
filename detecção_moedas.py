# Importando os pacotes necessários 
import cv2

# Carregando a imagem da memória
img = cv2.imread("set_de_moedas.jpeg")

# Exibindo a imagem original
cv2.imshow("Image", img)

# Convertendo a imagem para a escala de cinza 
"""
A maioria das operaões em processamento de imagem funcionam melhor em imagens
na escala de CINZA, isso ocorre pois diminui a quantidade de informação vinda da 
imagem.
"""
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicando um desfoque Gaussiano ns imagem
"""
Essa técnica suavisa o ruído na imagem antes da thresholding.
O segundo argumento é o tamanho do kernel - Um kernel maior resulta em mais desfoque
"""
blurred = cv2.GaussianBlur(gray,(7,7), 0)

# Aplicando thresholding de Otso à imagem

"""
O thresholding de Otsu é um método que escolhe automaticamente o melhor valor de 
thresholding entre o preto e o branco para uma imagem em escala de cinza. 
Note que nós fornecemos 0 como nosso valor de limiar inicial - isso é ignorado devido 
à flag cv2.THRESH_OTSU. A thresholding de Otsu é usada normalmente em imagens
bimodais, onde a imagem é composta por dois tipos distintos de pixels.
"""
threshold_value, thresh_inv = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
cv2.imshow("Thresholding", thresh_inv)
print(f"[INFO] otsu's thresholding value: {threshold_value}")

# Utilizando a imagem limiarizada como uma máscara na imagem original
"""
Isso fará com que apenas os pixels correspondentes aos pixels brancos na imagem 
limiarizada sejam visíveis.
"""
masked = cv2.bitwise_and(img, img, mask=thresh_inv)
cv2.imshow("Output", masked)

# Esperando o usuário apertar qualquer tecla para fechar a janela da imagem
cv2.waitKey(0)
