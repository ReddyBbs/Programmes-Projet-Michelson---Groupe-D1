# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:58:21 2024

@author: reddi
"""

import numpy as np
import cv2


def on_click(event, x, y, p1, p2):
    if event == cv2.EVENT_LBUTTONDOWN:
        global pxArray
        global intensityArray
        global clicked
        global width
        if not(clicked):
            pxArray.append((y,x))
            if len(pxArray) == 3:
                cv2.line(frame, (0, y), (width, y), (0, 0, 255), 1)
            else:
                cv2.line(frame, (x, 0), (x, height), (0, 0, 255), 1)


def play_from_file(filename='output.avi', delay=25):
    cap = cv2.VideoCapture(filename)
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        cv2.imshow('frame', frame)
      
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
        
    return


def intensity_graph_slice(filename='output.avi'):
    cap = cv2.VideoCapture(filename)
    global frame
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', on_click)
    global pxArray
    global clicked
    clicked = False
    pxArray = []
    
    
    global width, height
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    while cap.isOpened():
        ret, frame = cap.read()        
        
        if not ret:
            break
        
        if not(clicked):
            cv2.resizeWindow('frame', (width, height))
            while True:
                cv2.imshow('frame', frame)
                info = 'Clickez deux fois pour fixer les limites selon x, puis une fois pour'
                info2 = 'fixer y. Une fois fait, appuyez sur n\'importe quelle touche.'
                cv2.putText(frame, info, (15,height-25), cv2.FONT_HERSHEY_PLAIN , 1, (0,0,255))
                cv2.putText(frame, info2, (10,height-10), cv2.FONT_HERSHEY_PLAIN , 1, (0,0,255))
                if len(pxArray) == 3:
                    global x1, x2, y
                    (x1, x2, y) = pxArray[0][1], pxArray[1][1], pxArray[2][0]
                    clicked = True
                    pxLineArrayX = np.arange(x1, x2, step=1)
                    pxLineArrayY = np.array([y]*int(x2-x1))
                    pxLineArray = [(int(pxLineArrayY[k]), int(pxLineArrayX[k])) for k in range(int(x2-x1))]
                    
                    global intensityArray
                    intensityArray = [[].copy() for p in range(int(x2-x1))]

                if cv2.waitKey(1) != -1:
                    cv2.destroyAllWindows()
                    break
        
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for k in range(int(x2-x1)):
            intensityArray[k].append(float(frame[pxLineArray[k]]))
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    intensityArray = np.array(intensityArray)
    
    
    clicked = False
    
    return intensityArray



def graph_over_video(filename='output.avi', play=True):
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1/fps * 1e3) if play else 1
    
    global x1, x2, y
    
    I = intensity_graph_slice(filename=filename)
    I = I/np.max(I)
    
    maxFrame = np.shape(I)[1]
    I = I * height/4 
    I = np.array(I, dtype=np.int32)
    I = [np.array([[x+x1,height - I[x,k] - 10] for x in range(int(x2-x1))], dtype=np.int32) for k in range(maxFrame)]
    
    currentFrame = 0
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename.split('.')[0] + '_visualisation.avi', fourcc, fps, (width, height))

    
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if currentFrame >= maxFrame:
            break
        
        cv2.polylines(frame, [I[currentFrame]], False, (255, 255, 0), thickness=2)
        
        if not ret:
            break

        if play:
            cv2.imshow('frame', frame)
        out.write(frame)
        
        currentFrame += 1
      
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            play = False
            delay = 1
            cv2.destroyAllWindows()
    
    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()
        
    return


if __name__ == '__main__':
    graph_over_video(filename=input('De quel fichier voulez vous une vue en coupe ? '))



