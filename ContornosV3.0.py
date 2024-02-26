import numpy as np
import cv2 
import matplotlib.pyplot as plt

def radiusLen(_center, point):
    powx = np.power((_center[0] - point[0]), 2)
    powy = np.power((_center[1] - point[1]), 2)
    lenght = np.sqrt(powx + powy)
    
    return int(lenght)

def selectPoints(event, x, y, flags, params):
    global center, r_point, frame, pathdata, namevid
    #### Clic izquierdo ####
    if event == cv2.EVENT_LBUTTONDOWN:
        center = x, y
    
    if event == cv2.EVENT_RBUTTONDOWN:
        r_point = x, y
        
    if event == cv2.EVENT_MBUTTONDOWN:
        ######### Calculo del radio de la circunferencia #########
        radius = radiusLen(center, r_point)
        contour = (center[0], center[1], radius)
        cv2.destroyWindow("Imagen")
        
        ######### Dibuja el contorno seleccionado ##########
        cx, cy, r = contour
        print(contour)
        cv2.circle(frame, (cx,cy), r, (0, 255, 0), 2)
        cv2.circle(frame, (cx,cy), 1, (0, 0, 255), 3)
        cv2.imshow("Aproximacion", frame); cv2.waitKey(0)
        contour = np.array([contour])
        contour.tofile(pathdata + 'ContornoV' + namevid[0:2] + '.dat', sep = ' ')
            
        if contour is None:
            print('No se encontro circulo')
    
######### rutas de acceso a datos ########
pathvid = 'G:\\ControlChico5\\'
pathdata = 'G:\\Aproximaciones\\Circulos\\CP5\\'

######### Parametros #########
namevid = '91-GH010742.MP4'
initial_frame = 2000

######## Colocando Frame a Analizar ########
capture = cv2.VideoCapture(pathvid+namevid)
capture.set(cv2.CAP_PROP_POS_FRAMES, initial_frame)
success, frame = capture.read()

######## Muestra la imagen para seleccionar puntos #########
cv2.imshow("Imagen", frame)
center = cv2.setMouseCallback("Imagen", selectPoints)
cv2.waitKey(0)


    
capture.release()