#! /usr/bin/env python

import hilbert_curve as hc
from PIL import Image
import math
import wave
import numpy as np
from scipy.io import wavfile
import scipy.io

#Ime datoteke, ki jo hočemo prevajati v zvok
input_f='128x128W'
filler=''
simultano='-S-'
input_file = input_f+'.png'
output_wav = input_f+simultano+filler+'.wav'

num_seconds = 16

print("Input: "+input_f)

def generateSine(f,t):
	return ((math.sin(t/44100*2*math.pi*f)))

img = Image.open(input_file).convert("L")
pixels = img.load()
x,y = img.size

print ("Umeščanje pikslov po Pseudo-Hilbertovi krivulji")

output = []
i = 0

for i in range(0,x**2):
	hilbert = hc.d2xy(math.log(x*y,2),i)
	output.append(pixels[hilbert])

print ("Ustvarjanje zaporedja...")
outputAudio = [0]*(44100*num_seconds)

pixel_count = 0
for pixel in output:
	if pixel_count % 10 == 0:
		print (pixel_count,"pikslov kočanih od", x*y, end="\n")
	pixel_count += 1
	frequency = (pixel*8)+220
	for t in range(0,len(outputAudio)):
		outputAudio[t] += generateSine(frequency,t)

maxx=max(outputAudio)
minn=abs(min(outputAudio))
if maxx>=minn:
	ma=maxx
else:
	ma=minn

print("Umeščanje vrednosti med -1 in 1")
for i in range(0,len(outputAudio)):
	if i % 10000 == 0:
		print(i,"od", len(outputAudio), end="\n")
	outputAudio[i] = outputAudio[i]/ma

print("Generiranje wav datoteke.")
scipy.io.wavfile.write(output_wav,44100,np.asarray(outputAudio,dtype=float))
print("Končano")