import cv2
import numpy as np

# Valores iniciales (ejemplo para azul)
low_l = 54
high_l = 148
low_a = 124
high_a = 164
low_b = 25
high_b = 121

# Función vacía para los trackbars
def nothing(x):
    pass

# Crear ventana para los trackbars
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 600, 300)

# Crear trackbars
cv2.createTrackbar("Low L", "Trackbars", low_l, 255, nothing)
cv2.createTrackbar("High L", "Trackbars", high_l, 255, nothing)
cv2.createTrackbar("Low A", "Trackbars", low_a, 255, nothing)
cv2.createTrackbar("High A", "Trackbars", high_a, 255, nothing)
cv2.createTrackbar("Low B", "Trackbars", low_b, 255, nothing)
cv2.createTrackbar("High B", "Trackbars", high_b, 255, nothing)

# Captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a espacio de color LAB
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)

    # Obtener valores actuales de los trackbars
    low_l = cv2.getTrackbarPos("Low L", "Trackbars")
    high_l = cv2.getTrackbarPos("High L", "Trackbars")
    low_a = cv2.getTrackbarPos("Low A", "Trackbars")
    high_a = cv2.getTrackbarPos("High A", "Trackbars")
    low_b = cv2.getTrackbarPos("Low B", "Trackbars")
    high_b = cv2.getTrackbarPos("High B", "Trackbars")

    # Crear máscara con umbrales LAB
    lower = np.array([low_l, low_a, low_b])
    upper = np.array([high_l, high_a, high_b])
    mask = cv2.inRange(lab, lower, upper)

    # Operaciones morfológicas para limpiar la máscara
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Aplicar la máscara al frame original
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostrar resultados
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Color Detection", result)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()