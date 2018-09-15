from PIL import Image
import numpy as np
import cv2
#for i in range(1,25):
#	im = Image.open("img"+str(i)+".png")
#	rgb_im = im.convert('RGB')
#	rgb_im.save("img"+str(i)+".jpeg", "JPEG")
		
imgnext = 1
for i in range(1,25):
	if i % 2 == 1:
		im = Image.open("img"+str(i)+".jpeg")
		im = im.crop((0,0,1204,602))
		if imgnext < 10:
			im.save("img00"+str(imgnext)+".jpeg", "JPEG")
			imgnext += 1
		elif imgnext < 100:
			im.save("img0"+str(imgnext)+".jpeg", "JPEG")
			imgnext += 1
		elif imgnext < 1000:
			im.save("img"+str(imgnext)+".jpeg", "JPEG")
			imgnext += 1
	else:
		im = Image.open("img"+str(i)+".jpeg")
		for ii in range(0,7):
			if ii > 0:
				im = im.crop((100,0,1204-100*(ii),602))
			i3 = Image.new( 'RGB' , ( 1204 , 602 ) , (255,255,255) )
			i3.paste( im , (0,0) )
			if imgnext < 10:
				i3.save("img00"+str(imgnext)+".jpeg", "JPEG")
				imgnext += 1
			elif imgnext < 100:
				i3.save("img0"+str(imgnext)+".jpeg", "JPEG")
				imgnext += 1
			elif imgnext < 1000:
				i3.save("img"+str(imgnext)+".jpeg", "JPEG")
				imgnext += 1

