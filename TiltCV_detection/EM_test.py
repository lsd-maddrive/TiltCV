import cv2
import numpy as np
import matplotlib.pyplot as plt


bgr = cv2.imread("first.png")
Lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2Lab)

fig = plt.figure
# value = np.array([[0,0]])
value =[]

i = 0
pixel = Lab[:, :, 1:3]
print(pixel.shape)

print(range(len(pixel)))
for y in range(len(pixel)):
	for x in range(len(pixel[y])):
		
		
		value.append(pixel[y][x])
		plt.scatter(value[i][0],value[i][1],c='black',edgecolor ='none')
		i = i + 1


plt.show()	

while 1:
	
	cv2.imshow("1", Lab)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break