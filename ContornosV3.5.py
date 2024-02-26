import numpy as np
import cv2

def createWindow(_Wname, _frame):
    _h, width = _frame.shape[:2]
    ratio = width / 1280
    scale = 0.7
    thick = 2
    px, py = 50,50
    sep = 30
    
    if ratio > 1:
        scale = int(scale * ratio)
        thick = thick * int(ratio)
        px, py = (int(px*ratio), int(py*ratio))
        sep = int(sep*ratio)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(_frame, "LB = Center", (px, py), font, scale, (0,255,255), thick, cv2.LINE_AA)
    cv2.putText(_frame, "RB = Boundary", (px, py+sep), font, scale, (0,255,255), thick, cv2.LINE_AA)
    cv2.putText(_frame, "MB = Draw Circle", (px, py+2*sep), font, scale, (0,255,255), thick, cv2.LINE_AA)
    cv2.putText(_frame, "Wheel Up = Reset", (px, py+3*sep), font, scale, (0,255,255), thick, cv2.LINE_AA)
    cv2.namedWindow(_Wname, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(_Wname, (1280,720))
    cv2.moveWindow(_Wname, 179, 139)

def getFrame(full_path, _initial_frame):
    capture = cv2.VideoCapture(full_path)
    capture.set(cv2.CAP_PROP_POS_FRAMES, _initial_frame)
    success, _frame = capture.read()
    capture.release()
    
    return _frame

def radiusLen(_center, point):
    powx = np.power((_center[0] - point[0]), 2)
    powy = np.power((_center[1] - point[1]), 2)
    lenght = np.sqrt(powx + powy)
    
    return int(lenght)

def selectPoints(event, x, y, flags, params):
    global center, r_point, comp_path, frame, font, initial_frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    #### Clic izquierdo ####
    if event == cv2.EVENT_LBUTTONDOWN:
        center = x, y
        cv2.circle(frame, (center), 0, (0,255,0), 8)
        cv2.putText(frame, str(center), (center[0]-40,center[1]-20), font,
                    0.6, (0,255,0), 2, cv2.LINE_AA)
        cv2.imshow("Imagen", frame)
    
    if event == cv2.EVENT_RBUTTONDOWN:
        r_point = x, y
        cv2.circle(frame, (r_point), 0, (0,0,255), 8)
        cv2.putText(frame, str(r_point), (r_point[0]-40,r_point[1]-20), font,
                    0.6, (0,0,255), 2, cv2.LINE_AA)
        cv2.imshow("Imagen", frame)
        
    if event == cv2.EVENT_MBUTTONDOWN:
        ######### Calculo del radio de la circunferencia #########
        radius = radiusLen(center, r_point)
        contour = (center[0], center[1], radius)
        
        ######### Dibuja el contorno seleccionado ##########
        cx, cy, r = contour
        print(contour)
        cv2.circle(frame, (cx,cy), r, (0, 255, 255), 2)
        cv2.line(frame, center, r_point,(0,255,255),2)
        cv2.putText(frame, "R = " + str(radius), (center[0]+40, center[1]+20), font,
                    0.6, (0,255,255), 2, cv2.LINE_AA)
        cv2.imshow("Imagen", frame); cv2.waitKey(0)
        cv2.destroyAllWindows()
        contour = np.array([contour])
        # contour.tofile(pathdata + 'ContornoV' + namevid[0:2] + '.dat', sep = ' ')
    
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            frame = getFrame(comp_path, initial_frame)
            createWindow("Imagen", frame)
            cv2.imshow("Imagen", frame)
    
######### rutas de acceso a datos ########
pathvid = 'G:\\ControlChico5\\'
pathdata = 'G:\\Aproximaciones\\Circulos\\CP6\\'
namevid = '91-GH010742.MP4'
comp_path = pathvid + namevid

######### Parametros #########
initial_frame = 2000

######## Colocando Frame a Analizar ########
frame = getFrame(comp_path, initial_frame)

######## Muestra la imagen para seleccionar puntos #########
createWindow("Imagen", frame)
cv2.imshow("Imagen", frame)
center = cv2.setMouseCallback("Imagen", selectPoints)
cv2.waitKey(0)

    
