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

# Crear ventana principal
cv2.namedWindow("Control Panel")
cv2.resizeWindow("Control Panel", 1000, 700)

# Crear trackbars
cv2.createTrackbar("Low L", "Control Panel", low_l, 255, nothing)
cv2.createTrackbar("High L", "Control Panel", high_l, 255, nothing)
cv2.createTrackbar("Low A", "Control Panel", low_a, 255, nothing)
cv2.createTrackbar("High A", "Control Panel", high_a, 255, nothing)
cv2.createTrackbar("Low B", "Control Panel", low_b, 255, nothing)
cv2.createTrackbar("High B", "Control Panel", high_b, 255, nothing)

# Captura de video
cap = cv2.VideoCapture(0)

# Tamaños y posiciones
trackbar_height = 180
button_height = 40
button_width = 150
button_margin = 20
color_box_size = 200
color_box_margin = 20

# Función para manejar clics del mouse
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, color_name in enumerate(predefined_colors.keys()):
            bx = 20 + i * (button_width + button_margin)
            by = trackbar_height + 20
            
            if bx <= x <= bx + button_width and by <= y <= by + button_height:
                # Cargar valores predefinidos
                color_vals = predefined_colors[color_name]
                cv2.setTrackbarPos("Low L", "Control Panel", color_vals["low"][0])
                cv2.setTrackbarPos("High L", "Control Panel", color_vals["high"][0])
                cv2.setTrackbarPos("Low A", "Control Panel", color_vals["low"][1])
                cv2.setTrackbarPos("High A", "Control Panel", color_vals["high"][1])
                cv2.setTrackbarPos("Low B", "Control Panel", color_vals["low"][2])
                cv2.setTrackbarPos("High B", "Control Panel", color_vals["high"][2])

# Registrar callback del mouse
cv2.setMouseCallback("Control Panel", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a espacio de color LAB
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)

    # Obtener valores actuales de los trackbars
    low_l = cv2.getTrackbarPos("Low L", "Control Panel")
    high_l = cv2.getTrackbarPos("High L", "Control Panel")
    low_a = cv2.getTrackbarPos("Low A", "Control Panel")
    high_a = cv2.getTrackbarPos("High A", "Control Panel")
    low_b = cv2.getTrackbarPos("Low B", "Control Panel")
    high_b = cv2.getTrackbarPos("High B", "Control Panel")

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

    # Crear panel de control
    control_panel = np.zeros((700, 1000, 3), dtype=np.uint8)
    control_panel[:] = (50, 50, 50)  # Fondo gris oscuro
    
    # Dibujar sección de trackbars
    cv2.rectangle(control_panel, (10, 10), (990, trackbar_height), (80, 80, 80), -1)
    
    # Mostrar valores de los trackbars
    y_offset = 30
    cv2.putText(control_panel, f"L: {low_l}-{high_l}", (20, y_offset), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(control_panel, f"A: {low_a}-{high_a}", (20, y_offset + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    cv2.putText(control_panel, f"B: {low_b}-{high_b}", (20, y_offset + 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # Dibujar botones de colores predefinidos
    cv2.putText(control_panel, "Presets:", (20, trackbar_height + 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 1)
    
    for i, (color_name, _) in enumerate(predefined_colors.items()):
        x = 20 + i * (button_width + button_margin)
        y = trackbar_height + 20
        
        # Asignar color BGR para visualización
        if color_name == "Azul":
            bgr_color = (255, 0, 0)
        elif color_name == "Rojo":
            bgr_color = (0, 0, 255)
        elif color_name == "Verde":
            bgr_color = (0, 255, 0)
        elif color_name == "Amarillo":
            bgr_color = (0, 255, 255)
        
        cv2.rectangle(control_panel, (x, y), (x + button_width, y + button_height), bgr_color, -1)
        cv2.putText(control_panel, color_name, (x + 10, y + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Calcular y mostrar color detectado
    L_center = (low_l + high_l) // 2
    A_center = (low_a + high_a) // 2
    B_center = (low_b + high_b) // 2
    
    # Crear color en espacio LAB y convertir a BGR
    color_patch = np.zeros((color_box_size, color_box_size, 3), dtype=np.uint8)
    color_patch[:, :] = [L_center, A_center, B_center]
    color_patch_bgr = cv2.cvtColor(color_patch, cv2.COLOR_Lab2BGR)
    
    # Dibujar cuadro de color
    color_box_x = 1000 - color_box_size - color_box_margin
    color_box_y = trackbar_height + 20
    control_panel[color_box_y:color_box_y+color_box_size, 
                  color_box_x:color_box_x+color_box_size] = color_patch_bgr * 255
    
    # Etiqueta del cuadro de color
    cv2.putText(control_panel, "Color Detectado", 
                (color_box_x, color_box_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    
    # Mostrar valores LAB en el cuadro
    cv2.putText(control_panel, f"L: {L_center}", 
                (color_box_x + 10, color_box_y + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(control_panel, f"A: {A_center}", 
                (color_box_x + 10, color_box_y + 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(control_panel, f"B: {B_center}", 
                (color_box_x + 10, color_box_y + 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Mostrar imágenes de video en el panel
    display_height = 200
    display_width = 300
    
    # Redimensionar imágenes
    frame_disp = cv2.resize(frame, (display_width, display_height))
    mask_disp = cv2.resize(mask, (display_width, display_height))
    result_disp = cv2.resize(result, (display_width, display_height))
    
    # Convertir máscara a color para visualización
    mask_disp = cv2.cvtColor(mask_disp, cv2.COLOR_GRAY2BGR)
    
    # Posiciones para las miniaturas
    thumb_y = trackbar_height + button_height + 50
    
    # Original
    control_panel[thumb_y:thumb_y+display_height, 20:20+display_width] = frame_disp
    cv2.putText(control_panel, "Original", (20, thumb_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # Máscara
    control_panel[thumb_y:thumb_y+display_height, 20+display_width+20:20+display_width*2+20] = mask_disp
    cv2.putText(control_panel, "Mascara", (20+display_width+20, thumb_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # Resultado
    control_panel[thumb_y:thumb_y+display_height, 20+display_width*2+40:20+display_width*3+40] = result_disp
    cv2.putText(control_panel, "Resultado", (20+display_width*2+40, thumb_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Mostrar panel de control
    cv2.imshow("Control Panel", control_panel)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()