#from PIL import Image
import numpy as np
import cv2
#for i in range(1,25):
#	im = Image.open("img"+str(i)+".png")
#	rgb_im = im.convert('RGB')
#	rgb_im.save("img"+str(i)+".gif", "GIF")


f = open('inputs.txt','w')


imgnext = 1
nmid = 20
nshift = int(600/nmid)

for i in range(1,25):
	if i % 2 == 1:
		im = cv2.imread("img"+str(i)+".jpeg")
		if imgnext < 10:
			cv2.imwrite("img00"+str(imgnext)+".jpeg", im)
			f.write("file '"+"img00"+str(imgnext)+".jpeg"+"'\nduration 2\n")
			imgnext += 1
		elif imgnext < 100:
			cv2.imwrite("img0"+str(imgnext)+".jpeg", im)
			f.write("file '"+"img0"+str(imgnext)+".jpeg"+"'\nduration 2\n")
			imgnext += 1
		elif imgnext < 1000:
			cv2.imwrite("img"+str(imgnext)+".jpeg", im)
			f.write("file '"+"img"+str(imgnext)+".jpeg"+"'\nduration 2\n")
			imgnext += 1
	else:
		im = cv2.imread("img"+str(i)+".jpeg")
		for ii in range(0,nmid+1):
			if ii > 0:
				im = im[0:602, nshift:]
				im = cv2.copyMakeBorder(im,0,0,0,nshift,cv2.BORDER_CONSTANT,value=[255,255,255])
			if imgnext < 10:
				cv2.imwrite("img00"+str(imgnext)+".jpeg", im)
				if ii > 0:
					f.write("file '"+"img00"+str(imgnext)+".jpeg"+"'\nduration 0.05\n")
				else:
					f.write("file '"+"img00"+str(imgnext)+".jpeg"+"'\nduration 4\n")
				imgnext += 1
			elif imgnext < 100:
				cv2.imwrite("img0"+str(imgnext)+".jpeg", im)
				if ii > 0:
					f.write("file '"+"img0"+str(imgnext)+".jpeg"+"'\nduration 0.05\n")
				else:
					f.write("file '"+"img0"+str(imgnext)+".jpeg"+"'\nduration 4\n")
				imgnext += 1
			elif imgnext < 1000:
				cv2.imwrite("img"+str(imgnext)+".jpeg", im)
				if ii > 0:
					f.write("file '"+"img"+str(imgnext)+".jpeg"+"'\nduration 0.05\n")
				else:
					f.write("file '"+"img"+str(imgnext)+".jpeg"+"'\nduration 4\n")
				imgnext += 1
f.close()
