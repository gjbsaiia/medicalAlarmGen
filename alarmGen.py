#!/usr/bin/python
import os
import sys
import math
import wave
import struct

# change these as needed
argumentPath = "AlarmSpecifications.txt"
sampleRate = 8000.0 # this must be a float

# PRIORITY: 1 = HIGH, 0 = MEDIUM, -1 = LOW,
prior = {1: "HIGH",
		0: "MEDIUM",
		-1: "LOW"
}

# SIGNAL: True = Square, False = Sine
def sig(signal, pulseDur, srate, vol, freq):
	if(signal):
		return appendComboSquarewave(pulseDur, srate, vol, freq)
	else:
		return appendComboSinwave(pulseDur, srate, vol, freq)

def main():
	line = raw_input("Batch or manual? (b/m) ")
	if(line == "b"):
		param = readParam(argumentPath)
		batch(param)
	else:
		freq = float(raw_input("Enter alarm freqency: "))
		priority = int(raw_input("Enter priority of alarm (1=high, 0=medium, -1=low): "))
		if(priority > 0):
			pReq = "must be 75ms-200ms"
			wReq = "must be 50ms-125ms"
		else:
			pReq = "must be 125ms-250ms"
			wReq = pReq+", high prior. wait dur < this wait dur"
		pulseDur = float(raw_input("Enter pulse dur. ("+pReq+"): "))
		wDur = float(raw_input("Enter wait dur. ("+wReq+"): "))
		if(priority > 0):
			highPattern(True, freq, pulseDur, wDur)
			highPattern(False, freq, pulseDur, wDur)
		elif(priority == 0):
			mediumPattern(True, freq, pulseDur, wDur)
			mediumPattern(False, freq, pulseDur, wDur)
		else:
			lowPattern(True, freq, pulseDur, wDur)
			lowPattern(False, freq, pulseDur, wDur)

def readParam(path):
	with open(path, "r+") as file:
		lines = file.readlines()
	file.close
	params = []
	i = 0
	while i < len(lines):
		raw = lines[i].split()
		if raw[0] == "HIGH:" or raw[0] == "MEDIUM:" or raw[0] == "LOW:":
			splitt = lines[i+1].split()
			pulse = int(splitt[len(splitt)-1])
			splitt = lines[i + 2].split()
			wait = int(splitt[len(splitt)-1])
			params.append([pulse, wait])
		i += 1
	return params

def batch(param):
	freq = 300
	pulseDur = 125
	wDur = 50
	doAll(freq, param)
	freq = 400
	while(freq <= 1000):
		doAll(freq, param)
		freq += 200

def doAll(freq, param):
	highPattern(True, freq, param[0][0], param[0][1])
	highPattern(False, freq, param[0][0], param[0][1])
	mediumPattern(True, freq, param[1][0], param[1][1])
	mediumPattern(False, freq, param[1][0], param[1][1])
	lowPattern(True, freq, param[2][0], param[2][1])
	lowPattern(False, freq, param[2][0], param[2][1])

def highPattern(signal, freq, pulseDur, wDur):
	maudio = []
	srate = sampleRate
	vol = 0.75
	c = 4 * wDur
	name = genName(signal, int(freq), 1)
	i = 0
	while(i < 2):
		maudio += sig(signal, pulseDur, srate, vol, freq)
		maudio += appendSilence(wDur, srate)
		maudio += sig(signal, pulseDur, srate, vol, freq)
		maudio += appendSilence(wDur, srate)
		maudio += sig(signal, pulseDur, srate, vol, freq)
		maudio += appendSilence(2*wDur + c, srate)
		maudio += sig(signal, pulseDur, srate, vol, freq)
		maudio += appendSilence(wDur, srate)
		maudio += sig(signal, pulseDur, srate, vol, freq)
		if(i == 0):
			maudio += appendSilence(350, srate)
		i += 1
	saveWav(maudio, srate, name, 1)

def mediumPattern(signal, freq, pulseDur, wDur):
	maudio = []
	srate = sampleRate
	vol = 0.75
	name = genName(signal, int(freq), 0)
	maudio += sig(signal, pulseDur, srate, vol, freq)
	maudio += appendSilence(wDur, srate)
	maudio += sig(signal, pulseDur, srate, vol, freq)
	maudio += appendSilence(wDur, srate)
	maudio += sig(signal, pulseDur, srate, vol, freq)
	saveWav(maudio, srate, name, 0)

def lowPattern(signal, freq, pulseDur, wDur):
	maudio = []
	srate = sampleRate
	vol = 0.75
	name = genName(signal, int(freq), -1)
	maudio += sig(signal, pulseDur, srate, vol, freq)
	maudio += appendSilence(wDur, srate)
	maudio += sig(signal, pulseDur, srate, vol, freq)
	maudio += appendSilence(wDur, srate)
	saveWav(maudio, srate, name, -1)

def genName(signal, freq, priority):
	if(signal):
		fname = "multiSquare_"+str(freq)+"Hz_"+prior[priority]
	else:
		fname = "multiSine_"+str(freq)+"Hz_"+prior[priority]
	directory = "alarms/"+prior[priority]+"/"
	if(not os.path.isdir(os.getcwd()+"/"+directory)):
		os.makedirs(directory)
	name = directory+fname
	i = 0
	almost = duplicateNames(name, i)
	file_name = almost+".wav"
	return file_name

def duplicateNames(name, i):
	if(os.path.isfile(name+".wav")):
		i += 1
		if(i == 1):
			name = name+"_n"+str(i)
		else:
			split = name.split("_n")
			name = split[0]+"_n"+str(i)
		return duplicateNames(name, i)
	else:
		return name

def appendComboSquarewave(dur, srate, vol, freq):
	audio = []
	numSamples = dur * (srate / 1000.0)
	for x in range(int(numSamples)):
		y1 = squareFunc(vol, freq, srate, x)
		y2 = squareFunc(vol, 1.5 * freq, srate, x)
		y3 = squareFunc(vol, 2.5 * freq, srate, x)
		y4 = squareFunc(vol, 2 * freq, srate, x)
		y5 = squareFunc(vol, 3 * freq, srate, x)
		y6 = squareFunc(vol, 3.5 * freq, srate, x)
		y7 = squareFunc(vol, 4 * freq, srate, x)
		y8 = squareFunc(vol, 4.5 * freq, srate, x)
		yF = ((y1 + y4 + y5 + y7) - (y2 + y3 + y6 + y8))/3
		audio.append(yF)
	return audio

def appendComboSinwave(dur, srate, vol, freq):
	audio = []
	numSamples = dur * (srate / 1000.0)
	for x in range(int(numSamples)):
		y1 = sinFunc(srate, vol, freq, x)
		y2 = sinFunc(srate, vol, 2*freq, x)
		y3 = sinFunc(srate, vol, 2.5*freq, x)
		y4 = sinFunc(srate, vol, 1.5*freq, x)
		yF = (y1 + y2 + y3 + y4)/3
		audio.append(yF)
	return audio

def appendSilence(dur, srate):
	audio = []
	numSamples = dur * (srate / 1000.0)
	for x in range(int(numSamples)):
	    audio.append(0.0)
	return audio

def sinFunc(srate, vol, freq, x):
	y = vol * math.sin(2 * math.pi * freq * ( x / srate ))
	return y

def squareFunc(vol, freq, srate, x):
	y = (2*vol/math.pi)*math.atan(math.sin((2*math.pi*freq) * (x/srate) ))
	return y

def saveWav(audio, srate, name, priority):
	wav_file=wave.open(name,"w")
	nchannels = 1
	sampwidth = 2
	nframes = len(audio)
	comptype = "NONE"
	compname = "not compressed"
	wav_file.setparams((nchannels, sampwidth, srate, nframes, comptype, compname))
	for sample in audio:
	    wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))
	wav_file.close()
	return

#Execute the wrapper
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print 'Interrupted'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
