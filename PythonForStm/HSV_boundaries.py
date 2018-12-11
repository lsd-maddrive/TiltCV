import cv2
import numpy as np

#Что бы заполнить Trackbar
def nothing(x):
	pass

#Получаем картинку
image_RGB=cv2.imread('RGB.png')

#Выводим картинку на экран
cv2.imshow('Original',image_RGB)

#Преобразовываем в формат HSV и в нужные размеры картинки
image_HSV=cv2.cvtColor(image_RGB, cv2.COLOR_RGB2HSV)	
image_HSV = cv2.resize(image_HSV,(480,360))

#Создание окна в котором создаются последующие виджеты
cv2.namedWindow('image')

#Создание ползунков и их значение
cv2.createTrackbar('DownH','image', 0, 255, nothing)
cv2.createTrackbar('DownS','image', 0, 255, nothing)
cv2.createTrackbar('DownV','image', 0, 255, nothing)

cv2.createTrackbar('UpH','image', 255, 255, nothing)
cv2.createTrackbar('UpS','image', 255, 255, nothing)
cv2.createTrackbar('UpV','image', 255, 255, nothing)




while (1):
	
	#Снимаем значение ползунков отвечающих за нижние границы
	DownH = cv2.getTrackbarPos('DownH','image')
	DownS = cv2.getTrackbarPos('DownS','image')
	DownV = cv2.getTrackbarPos('DownV','image')
	#Снимаем значение ползунков отвечающих за верхние границы
	UpH = cv2.getTrackbarPos('UpH','image')
	UpS = cv2.getTrackbarPos('UpS','image')
	UpV = cv2.getTrackbarPos('UpV','image')

	#Создаем многомерные массивы для верхний и нижних границ
	downArray = np.array([DownH, DownS, DownV])
	upArray = np.array([UpH, UpS, UpV])

	#Получаем выделенное изображение в заданных пределлах 
	mask = cv2.inRange(image_HSV,downArray,upArray)

	#Выводим результат
	cv2.imshow('image',mask)

	if cv2.waitKey(30)==27:
		break
