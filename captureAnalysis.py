# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 16:49:20 2024

@author: reddi
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import recordingModule as rcd
from datetime import datetime

#%% Fonctions préliminaires

def nothing(x):
    pass


def on_click(event, x, y, p1, p2):
    if event == cv2.EVENT_LBUTTONDOWN:
        global pxArray
        global intensityArray
        intensityArray.append([].copy())
        pxArray.append((y,x))
        cv2.circle(frame, (x, y), 8, (0, 0, 255), 1)
        cv2.line(frame, (x - 15, y), (x + 15, y), (0, 0, 255), 1)
        cv2.line(frame, (x, y - 15), (x, y + 15), (0, 0, 255), 1)



#%% Analyse de vidéos

def intensity_graph(filename='output.avi'):
    cap = cv2.VideoCapture(filename)
    global intensityArray
    intensityArray = []
    global frame
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', on_click)
    global pxArray
    clicked = False
    pxArray = []
    
    weights = np.array([[.01, .02, .04, .02, .01],
                        [.02, .04, .08, .04, .02],
                        [.04, .08, .16, .08, .04],
                        [.02, .04, .08, .04, .02],
                        [.01, .02, .04, .02, .01]])
    

    
    while cap.isOpened():
        ret, frame = cap.read()
        
        
        if not ret:
            break
        
        if not(clicked):
            while True:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) != -1:
                    clicked = True
                    cv2.destroyAllWindows()
                    break
        
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for k in range(len(pxArray)):
            y, x = pxArray[k]
            intensityArray[k].append(np.average(frame[y-2:y+3,x-2:x+3], weights=weights))

    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
        
    clicked = False
    
    return intensityArray



def graphAnalysis(I, divSize=0, rangeFactor=10):
    if divSize:
        if len(I)>divSize:
            m = len(I)//2 
            return graphAnalysis(I[:m]) + graphAnalysis(I[m:])
    
    mean = (max(I) + min(I))/2
    meanRange = (max(I) - min(I))/rangeFactor
    
    crossingNumber = 0
    
    for k in range(len(I)-1):
        if I[k] < I[k+1]:
            if (I[k]-(mean + meanRange))*(I[k+1]-(mean + meanRange)) < 0 :
                crossingNumber += 1
        else:
            if (I[k]-(mean - meanRange))*(I[k+1]-(mean - meanRange)) < 0 :
                crossingNumber += 1
    
    
    return crossingNumber/2


#%% Fonctions complètes (Acquisition et analyse)

def data_acquisition(index=0, fileName='output.avi', res=(640,480), fps=60., smoothing=0, plot=True, record=True):
    if record:
        fps= float(input('Framerate = '))
        res = (int(input('width = ')), int(input('height = ')))
        slowfactor = float(input('Slow factor = '))
        rcd.record_from_camera(index=index, res=res, fps=fps, filename=fileName, slowmow=slowfactor)
    
    if not(rcd.recording):
        return None
    
    I = intensity_graph(filename=fileName)
    
    if plot:
        plt.plot(range(len(I[0])), I[0])
        plt.show()
    
    return I


def acquisitionUI():
    recordS = input('Voulez vous utiliser un fichier déjà enregistré ? y/n | ')
    while not(recordS in ['y','n']): 
        recordS = input('Entrée invalide \n Voulez vous utiliser un fichier déjà enregistré ? y/n | ')
    record = (recordS == 'n')
    
    plot = input('Voulez vous afficher les données sous forme de graphique ? \n' +
                 'Il est conseillé de le faire s\'il s\'agit de la première analyse des données,' +
                 ' afin de paramétrer aux mieux l\'analyse des données. \n y/n | ')
    while not(plot in ['y','n']): 
        plot = input('Entrée invalide \n Voulez vous afficher les données sous forme de graphique ? y/n | ')
    plot = (plot == 'y')
    
    if record:
        index = int(input('Quelle caméra voulez-vous utiliser ? (donnez son indice) | '))
        I =  data_acquisition(index=index, fileName='{}.avi'.format(datetime.now().strftime("%Y%m%d_%H%M%S")), record=True, plot=plot)
    
    else:
        fileName = input('Quel fichier voulez vous analyser ? | ')
        try:
            f = open(fileName, 'r')
            f.close()
        except:
            print("Une erreur s'est produite, vérifiez bien que le fichier demandé est situé dans le bon répertoire.")
            return
        I = data_acquisition(fileName=fileName, record=False, plot=plot)
    
    if not(I):
        return
    
    
    rangeFactor = float(input("Portion de l'amplitude pour l'intervalle anti-bruit (en cas de doute, mettez 4) = "))
    while rangeFactor <= 0:
        rangeFactor = float(input("Entrée invalide, veuillez donner un réel strictement positif | "))
    divSize = int(input('Taille maximum des sous-échantillons (doit être suffisamment grande pour que les sous-échantillons soit exploitables) = '))
    startFrame = int(input('Image de départ de l\'analyse = '))
    endFrame = int(input('Image de fin de l\'analyse (comptée depuis la fin de l\'échantillon) = '))
    crossingNumberArray = [graphAnalysis(I[k][startFrame:-endFrame], divSize=divSize, rangeFactor=rangeFactor) for k in range(len(I))]
    print('(Moyenne, Ecart-type, Nombre de points suivis)')
    return np.mean(crossingNumberArray), np.std(crossingNumberArray), len(crossingNumberArray)



if __name__ == '__main__':
    print(acquisitionUI())
    
    

    



