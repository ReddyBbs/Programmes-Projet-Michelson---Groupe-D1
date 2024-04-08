Les deux seuls programmes faits pour être exécutés sont captureAnalysis.py et ringVisualiser.py, le troisième (recordingModule.py) servant de module contenant les fonctions gérant l'enregistrement et l'affichage vidéo. 
Afin de s'assurer que les programmes fonctionnent au mieux, il est recommandé de les exécuter directement depuis un terminal ouvert à l'emplacement des fichiers (sous Windows, à l'aide de la commande py nom_du_fichier.py). 

captureAnalysis.py : permet d'enregistrer et d'analyser des vidéos
  - Par défaut, ce programme enregistre les vidéos en 1280x720p avec une fréquence de 60ips.
  - Pour enregistrer une vidéo, une fois l'interface ouverte, il faut passer la trackbar "Recording" sur la valeur 1, avant d'appuyer sur la touche q pour lancer l'enregistrement. Une fois celui-ci lancé, rappuyer sur la touche q le stoppe et enregistre la vidéo filmée au format avi, nommée à l'aide de la date de de l'heure de l'enregistrement.
  - Pour effectuer un comptage de franges, une fois l'interface correspondante ouverte, il faut cliquer sur l'ensemble des points à suivre, puis appuyer sur une touche du clavier quelconque. Si aucun point n'est sélectionné, le programme s'arrêtera là, renvoyant None.

ringVisualiser : permet d'afficher un suivi en coupe de l'intensité lumineuse d'une vidéo 
