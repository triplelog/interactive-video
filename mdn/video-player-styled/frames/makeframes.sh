for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
do
	#curl https://server0.calculuscollege.com/media/new/b34e8b10-5bb5-438a-942b-cc91a9f68bc5ex${i}.png -o img$((i + 1)).png
	convert -crop 1204x602+0+0 img$((i + 1)).png img$((i + 1)).png
done
for i in 1
do
	convert -crop 1204x602+0+0 img$((i * 2 - 1)).png img00$((i * 8 - 7)).png
	convert -crop 1204x602+0+0 img$((i * 2)).png img00$((i * 8 - 6)).png
	convert img$((i * 2)).png -crop 1104x602+100+0 -background white -extent 1204x602 -write img00$((i * 8 - 5)).png \
	-crop 1004x602+200+0 -background white -extent 1204x602 -write img00$((i * 8 - 4)).png \
	-crop 904x602+300+0 -background white -extent 1204x602 -write img00$((i * 8 - 3)).png \
	-crop 804x602+400+0 -background white -extent 1204x602 -write img00$((i * 8 - 2)).png \
	-crop 704x602+500+0 -background white -extent 1204x602 -write img00$((i * 8 - 1)).png \
	-crop 604x602+600+0 -background white -extent 1204x602 img00$((i * 8)).png
done
convert -crop 1204x602+0+0 img3.png img009.png
convert -crop 1204x602+0+0 img4.png img010.png
convert -crop 1104x602+100+0 -background white -extent 1204x602 img4.png img011.png
convert -crop 1004x602+200+0 -background white -extent 1204x602 img4.png img012.png
convert -crop 904x602+300+0 -background white -extent 1204x602 img4.png img013.png
convert -crop 804x602+400+0 -background white -extent 1204x602 img4.png img014.png
convert -crop 704x602+500+0 -background white -extent 1204x602 img4.png img015.png
convert -crop 604x602+600+0 -background white -extent 1204x602 img4.png img016.png
for i in 2 3 4 5 6 7 8 9 10 11 12
do
	convert -crop 1204x602+0+0 img$((i * 2 - 1)).png img0$((i * 8 - 7)).png
	convert -crop 1204x602+0+0 img$((i * 2)).png img0$((i * 8 - 6)).png
	convert img$((i * 2)).png -crop 1104x602+100+0 -background white -extent 1204x602 -write img0$((i * 8 - 5)).png \
	-crop 1004x602+200+0 -background white -extent 1204x602 -write img0$((i * 8 - 4)).png \
	-crop 904x602+300+0 -background white -extent 1204x602 -write img0$((i * 8 - 3)).png \
	-crop 804x602+400+0 -background white -extent 1204x602 -write img0$((i * 8 - 2)).png \
	-crop 704x602+500+0 -background white -extent 1204x602 -write img0$((i * 8 - 1)).png \
	-crop 604x602+600+0 -background white -extent 1204x602 img0$((i * 8)).png
done
ffmpeg -framerate 1 -i img%03d.png output.mp4
ffmpeg -i output.mp4 -c:v libvpx -crf 10 -b:v 1M -c:a libvorbis output.webm
