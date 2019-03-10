#! /usr/bin/env python

import hilbert_curve as hc
from PIL import Image
import math
import wave
import numpy as np
from scipy.io import wavfile
import scipy.io

#Ime datoteke, ki jo hočemo prevajati v zvok
input_f='128x128B'
filler='4096s'
konsekutivno='-K-'
input_file = input_f+'.png'
output_wav =  input_f+konsekutivno+filler+'.wav'
output_txt = input_f+konsekutivno+filler+'-Before.txt'
output_txt1 = input_f+konsekutivno+filler+'-After.txt'

num_seconds = 4096
length = (num_seconds*44100)

print("Input: "+input_f)

#Funkcija, ki naredi sinusoide
def generateSine(f,t):
	return ((math.sin(t/44100*2*math.pi*f)))

#Zapis slike v spomin
img = Image.open(input_file).convert("L")
pixels = img.load()
x,y = img.size

output = []
i = 0

print ("Umeščanje pikslov po Pseudo-Hilbertovi krivulji")
for i in range(0,x**2):
	hilbert = hc.d2xy(math.log(x*y,2),i)
	output.append(pixels[hilbert])

print ("Generiranje sinusoid")
outputAudio = [0]*length

startA=0
stopA=0
chop1 = int(length/len(output))
pixel_count = 0

#Generiranje sinusoid za različne frekvence
for pixel in output:
	if pixel_count % 10 == 0:
		print (pixel_count,"pixels completed out of", x*y, end="\n")

	pixel_count += 1
	frequency = (pixel*8)+220

	startA = (pixel_count-1)*chop1
	stopA = startA + chop1 - 1

	if stopA>length:
		stopA = length

	for t in range(startA,stopA):
		outputAudio[t] += generateSine(frequency,t)

#Izpis zaporedja, ki zapiše zaporedje pred umeščanjem vrednosti med -1 in 1
#np.savetxt(output_txt,outputAudio)

maxx=max(outputAudio)
minn=abs(min(outputAudio))
if maxx>minn:
	mapp = maxx
else:
	mapp = minn

print("Umeščanje vrednosti med -1 in 1")
for i in range(0,len(outputAudio)):
	if i % 10000 == 0:
		print(i,"od", len(outputAudio), end="\n")
	outputAudio[i] = outputAudio[i] / mapp

#Izpis zaporedja, ki zapiše wav datoteko
#np.savetxt(output_txt1,outputAudio)

print("Generiranje wav datoteke.")
scipy.io.wavfile.write(output_wav,44100,np.asarray(outputAudio,dtype=float))
print("Konec")