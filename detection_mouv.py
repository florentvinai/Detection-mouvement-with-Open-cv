# Utilisation
# python detection_mouv.py
# python detection_mouv.py --video videos/example_01.mp4
#  python detection_mouv.py --video rtsp2://@ip:/video/

# importe les packages necessaire
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import numpy as np
import cv2

# construction de l' argument parser et parse
# Possibilite d'utiliser un fichier video mp4 ou
# de faire du streaming sur un flux disponible sur @ip / video ( depend de la camera ip)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# si il nya pas d'argument video , alors on lis sur la webcam
if args.get("video", None) is None:
	#src=0 -> l	 webcam
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# sinon  on lit a le fichier ou le streamin donne en argument
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# Boucle infini
# On fera les action a l'interieur de la boucle tant que le flux video n'est pas fini
# ou que l'utilisateur n'a pas appuyer sur q pour quitter
# ----------------------------------------------------------------------------
while True:
	# On saisie/lit  la frame video
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	#on initialize le texte de detetcion
	text = "Vide"

	# si the frame  ne peut pas etre lus,alors c 'est la fin de la video
	# ------------------------------------------------------------------
	if frame is None:
		break

	# On redimensionne Window / the frame,
	frame = imutils.resize(frame, width=400)

	# pre-traitement :On transforme/converti la frame en gris
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 

	# pre-traitement : On va flouter l'image avant de determiner les contours
	gray = cv2.blur(gray, (15,15))

	#   Le Filtrage de l'image peut etre par d'autres fonctions Gaussian/ bilateralFilter()
	#    gray = cv2.GaussianBlur(gray, (21, 21), 0)
	

	# SI la 1 frame is None, on l'initialize 
	# Cela veut que l'on prend la FirstFrame comme l'immage du decor
	# Voir dans le CR la methode de detection de mouvement
	#
	if firstFrame is None:
		firstFrame = gray
		continue

	# Pour detecter le mouvement 
	# on calcule la difference entre la frame courante et la 1 frame de reference pre-traitee
	# 
	# resultat dans la matrice frameDelta
	frameDelta = cv2.absdiff(firstFrame, gray)

	# Pre-traitement de la matrice Delta
	# nous allons binariser la frameDelta des images noirs et blancs 
	# selon la methode THRESH_BINARY
	# par rapport a la valeur d'un seuil 20, 155
	# resultat dans thresh
	thresh = cv2.threshold(frameDelta, 20, 155, cv2.THRESH_BINARY)[1]

	# pre-traitement : dilate l'image seuillééé et rempli les trous ( voir fonction dilate CV2) 
	# resultat dans la matrice thresh
	thresh = cv2.dilate(thresh, None, iterations=1)
	
	# pre-traitement : trouve les contrours de l'image seuillée 
	# renvoi le resultat dans cnts
	# suivant la methode cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE
	# voir la fonction CV2 findContours
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# Boucle npour chaque contours
	for c in cnts:
		# si le  contour is trop Petit , ignore itrien faire
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# on calcule les bords du contour,
		# on renvoi les 4 points du contours
		(x, y, w, h) = cv2.boundingRect(c)

		# ON dessine sur l'image frame le rectangle/cercle du contour
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#cv2.circle(frame, (x + w, y + h), (x -w ), (0, 255, 0), 1)

		# on met a jour le texte
		text = "Presence"

	# on ecrit le  L'etat : text  sur l'image frame
	#   
	cv2.putText(frame, "Etat : {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

	# on ecrit le  TITRE SUR Ll'image frame
	#   
	cv2.putText(frame, "Projet Merad test detection", (330, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

	# on ecrit la date sur l'image frame
	#   
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

	# On montre le resultat de 3 images 
	# on affiche limage avec les contours des objet en mouvement
	cv2.imshow("Flux de securite", frame)
	# on affiche limage SEUILLEEE 5 NOIR SI AUCUN MVMT
	cv2.imshow("Declenchement", thresh)
	# on affiche limage DIFFERENCE ENTRE LIMAGE SEUILLE ET LA REFERENCE  
	cv2.imshow("Difference de flux", frameDelta)
	
	# ON ENREGISTRE SI CLAVIER est pressee
	key = cv2.waitKey(1) & 0xFF

	# SI LETTRE Q ENFONCEE ON SORT DE LA BOUCLE
	if key == ord("q"):
		break

# on libere toutes les ressources et objet proprement 
# avant de sortir du programme
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
