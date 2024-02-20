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

	# pre-traitement :On transforme/converti la frame en HSV (color)
	#-------------------------------------------------------
	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# On specifie la zone de couleur a detecter 
	# define range of blue color in HSV pour la fonction CV2 Inrange
	# Zone basse : 
	# ZOne Haute : 
	# ------------------------------------

	lower_blue = np.array([90,0,0])
	upper_blue = np.array([110,255,255])

	# ON cree le masque avec la zone de bleur specifiée
	#
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	# On recup la sous image defini par le mask et l'image frame
	res = cv2.bitwise_and(frame,frame, mask= mask)


	# On converti la nouvelle imae en GRAY
	gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

	# pre-traitement : On va flouter l'image avant de determiner les contours
	gray = cv2.blur(gray, (15,15))

	if firstFrame is None:
		firstFrame = gray
		continue

	# on calcule la difference entre la frame courante et la 1 frame de reference pre-traitee
	# resultat dans la matrice frameDelta
	frameDelta = cv2.absdiff(firstFrame, gray)

	thresh = cv2.threshold(frameDelta, 50,180, cv2.THRESH_BINARY_INV)[1]

	# pre-ptraitement : dilate l'image seuillééé et rempli les trous ( voir fonction dilate CV2) 
	# resultat dans la matrice thresh
	thresh = cv2.dilate(thresh, None, iterations=1)

	cv2.imshow('frame',frame)
	cv2.imshow('gr',res)
	
	cv2.imshow('framedelta',frameDelta)
	cv2.imshow('thresh',thresh)

	# ON ENREGISTRE SI CLAVIER est pressee
	key = cv2.waitKey(1) & 0xFF

	# SI LETTRE Q ENFONCEE ON SORT DE LA BOUCLE
	if key == ord("q"):
		break

# on libere toutes les ressources et objet proprement 
# avant de sortir du programme
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
