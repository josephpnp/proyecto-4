import cv2
import numpy as np

# Valores iniciales (ejemplo para azul)
low_l = 54
high_l = 148
low_a = 124
high_a = 164
low_b = 25
high_b = 121

# Colores predefinidos (en formato LAB)
predefined_colors = {
    "Azul": {"low": [54, 124, 25], "high": [148, 164, 121]},
    "Rojo": {"low": [20, 150, 100], "high": [200, 255, 255]},
    "Verde": {"low": [30, 0, 0], "high": [150, 120, 150]},
    "Amarillo": {"low": [80, 0, 150], "high": [180, 150, 255]}
}

# Función vacía para los trackbars
def nothing(x):
    pass

# Crear ventana para los trackbars
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 800, 400)

# Crear trackbars
cv2.createTrackbar("Low L", "Trackbars", low_l, 255, nothing)
cv2.createTrackbar("High L", "Trackbars", high_l, 255, nothing)
cv2.createTrackbar("Low A", "Trackbars", low_a, 255, nothing)
cv2.createTrackbar("High A", "Trackbars", high_a, 255, nothing)
cv2.createTrackbar("Low B", "Trackbars", low_b, 255, nothing)
cv2.createTrackbar("High B", "Trackbars", high_b, 255, nothing)

# Crear ventana para el color detectado
cv2.namedWindow("Color Detectado")
cv2.resizeWindow("Color Detectado", 200, 200)

# Captura de video
cap = cv2.VideoCapture(0)

# Crear imagen para botones
buttons_bg = np.zeros((60, 800, 3), dtype=np.uint8)
button_width = 150
button_height = 40
button_margin = 20
button_positions = {}

# Dibujar botones iniciales
for i, (color_name, _) in enumerate(predefined_colors.items()):
    x = i * (button_width + button_margin) + button_margin
    y = 10
    button_positions[color_name] = (x, y, button_width, button_height)
    
    # Asignar color BGR para visualización
    if color_name == "Azul":
        bgr_color = (255, 0, 0)
    elif color_name == "Rojo":
        bgr_color = (0, 0, 255)
    elif color_name == "Verde":
        bgr_color = (0, 255, 0)
    elif color_name == "Amarillo":
        bgr_color = (0, 255, 255)
    
    cv2.rectangle(buttons_bg, (x, y), (x + button_width, y + button_height), bgr_color, -1)
    cv2.putText(buttons_bg, color_name, 
                (x + 10, y + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (255, 255, 255), 2)

# Función para manejar clics del mouse
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for color_name, (bx, by, bw, bh) in button_positions.items():
            if bx <= x <= bx + bw and by <= y <= by + bh:
                # Cargar valores predefinidos
                color_vals = predefined_colors[color_name]
                cv2.setTrackbarPos("Low L", "Trackbars", color_vals["low"][0])
                cv2.setTrackbarPos("High L", "Trackbars", color_vals["high"][0])
                cv2.setTrackbarPos("Low A", "Trackbars", color_vals["low"][1])
                cv2.setTrackbarPos("High A", "Trackbars", color_vals["high"][1])
                cv2.setTrackbarPos("Low B", "Trackbars", color_vals["low"][2])
                cv2.setTrackbarPos("High B", "Trackbars", color_vals["high"][2])

# Registrar callback del mouse
cv2.setMouseCallback("Trackbars", mouse_callback)

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
    
    # Mostrar botones
    cv2.imshow("Trackbars", buttons_bg)
    
    # Calcular y mostrar color detectado (promedio de los límites)
    L_center = (low_l + high_l) // 2
    A_center = (low_a + high_a) // 2
    B_center = (low_b + high_b) // 2
    
    # Crear color en espacio LAB y convertir a BGR
    color_patch = np.zeros((200, 200, 3), dtype=np.uint8)
    color_patch[:, :] = [L_center, A_center, B_center]
    color_patch_bgr = cv2.cvtColor(color_patch, cv2.COLOR_Lab2BGR)
    
    # Mostrar valores LAB
    cv2.putText(color_patch_bgr, f"L: {L_center} A: {A_center} B: {B_center}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    cv2.imshow("Color Detectado", color_patch_bgr)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()