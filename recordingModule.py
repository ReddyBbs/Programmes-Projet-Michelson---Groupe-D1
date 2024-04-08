# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 08:58:06 2024

@author: reddi
"""

import cv2

recording = True


# N'execute aucun code, mais est nécessaire pour le fonctionnement des trackbars
def nothing(x):
    pass



def display_from_camera(index=0, res=(640,480), fps=60., filename='output.avi', codec='XVID', grayscale=True):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
    cap.set(cv2.CAP_PROP_FPS, fps)
    
    
    cont = cap.get(cv2.CAP_PROP_CONTRAST)
    lum = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    gain = cap.get(cv2.CAP_PROP_GAIN)
        
    cv2.namedWindow('frame')

    cv2.createTrackbar('Grayscale', 'frame', int(grayscale), 1, nothing)
    cv2.createTrackbar('Contrast', 'frame', int(cont)*10, 1000, nothing)
    cv2.createTrackbar('Brightness', 'frame', int(lum)*10, 1000, nothing)
    cv2.createTrackbar('Gain', 'frame', int(gain)*10, 1000, nothing)
    

    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        
        if ret==True:
            
            
            gain = cv2.getTrackbarPos('Gain', 'frame')
            lum = cv2.getTrackbarPos('Brightness', 'frame')
            cont = cv2.getTrackbarPos('Contrast', 'frame')
            grayscale = bool(cv2.getTrackbarPos('Grayscale', 'frame'))

                
            cap.set(cv2.CAP_PROP_CONTRAST, cont/10)
            cap.set(cv2.CAP_PROP_BRIGHTNESS, lum/10)
            cap.set(cv2.CAP_PROP_GAIN, gain/10)
            
            if cv2.waitKey(1) & 0xFF == ord('g'):
                grayscale = not(grayscale)
                cv2.setTrackbarPos('Grayscale', 'frame', int(grayscale))
                

            
            if grayscale:
                # Switch the frame to grayscale and back to BGR for encoding
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            
            # Write the captured frame in the output file and display it
            cv2.imshow('frame', frame)
            

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        else:
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return



def record_from_camera(index=0, res=(640,480), fps=60., filename='output.avi', codec='XVID', grayscale=True, slowmow=1):
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
    cap.set(cv2.CAP_PROP_FPS, fps)
    
    cont = cap.get(cv2.CAP_PROP_CONTRAST)
    lum = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    gain = cap.get(cv2.CAP_PROP_GAIN)
        
    cv2.namedWindow('frame')

    # Création des trackbars permettant de modifier les paramètres vidéo
    recName = 'Recording'
    cv2.createTrackbar(recName, 'frame', 0, 1, nothing)
    cv2.createTrackbar('Grayscale', 'frame', int(grayscale), 1, nothing)
    cv2.createTrackbar('Contrast', 'frame', int(cont)*10, 1000, nothing)
    cv2.createTrackbar('Brightness', 'frame', int(lum)*10, 1000, nothing)
    cv2.createTrackbar('Gain', 'frame', int(gain)*10, 1000, nothing)
    
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    
    global recording
    recording = False
    
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        
        if ret==True:
            
            gain = cv2.getTrackbarPos('Gain', 'frame')
            lum = cv2.getTrackbarPos('Brightness', 'frame')
            cont = cv2.getTrackbarPos('Contrast', 'frame')
            grayscale = bool(cv2.getTrackbarPos('Grayscale', 'frame'))
            recording = bool(cv2.getTrackbarPos(recName, 'frame'))
            
            cap.set(cv2.CAP_PROP_CONTRAST, cont/10)
            cap.set(cv2.CAP_PROP_BRIGHTNESS, lum/10)
            cap.set(cv2.CAP_PROP_GAIN, gain/10)
            
            if grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Displays the frame
            cv2.imshow('frame', frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        else:
            break
    
    
    cv2.destroyAllWindows()
    
    if not recording:
        cap.release()
        return
    
    
    cv2.namedWindow('frame')
    out = cv2.VideoWriter(filename,fourcc, fps/slowmow, res)


    if grayscale:
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret==True:
                # Changes the frame to grayscale and then back to RGB for encoding
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                
                # Write the captured frame in the output file and display it
                out.write(frame)
                cv2.imshow('frame', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            else:
                break
        
    else :
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret==True:
                # Write the captured frame in the output file and display it
                out.write(frame)
                cv2.imshow('frame', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            else:
                break
    
    # When everything done, release the capture
    cap.release()
    if recording:
        out.release()
    cv2.destroyAllWindows()
    return


def camera_properties(index=0):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cont = cap.get(cv2.CAP_PROP_CONTRAST)
    lum = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    gain = cap.get(cv2.CAP_PROP_GAIN)
    return cont, lum, gain
    


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




