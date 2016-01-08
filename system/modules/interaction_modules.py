# -*- coding: utf-8 -*-
import sys

def progress(*args):#for logging
	for arg in args:
		print(arg, end=' ', sep=" ")
	print()

def warn(*args):
	for arg in args:
		print("\033[31m"+arg+"\033[0m", end=' ', sep=" ")
	print()
	
def commandline(*args):
	for arg in args:
		print(arg, end=' ', sep=" ")
	print()

def overwrite(*args):
	return areyousure("Do you want to overwrite the file?", *args)

def areyousure(confirmation, *args):
	warn(*args)
	while True:
		a = input(confirmation+" (y/n) > ")
		if a == "y":
			return True
		elif a == "n":
			return False

def get_progressbar_str(progress):
	MAX_LEN = 30
	BAR_LEN = int(MAX_LEN * progress)
	return ('[' + '=' * BAR_LEN + ('>' if BAR_LEN < MAX_LEN else '') + ' ' * (MAX_LEN-BAR_LEN) + '] %.1f%%' % (progress * 100.0))

def progress_bar2(k, length):
	progress = float(k) / length
	sys.stderr.write('\r\033[K' + get_progressbar_str(progress))
	sys.stderr.flush()

def show_logo_star():
	length = 120
	sentence = "UTab for PDA ver3.1"
	base = "-"*length
	for k, char in enumerate(reversed(sentence)):
		for i in range(int(length/2)+int(len(sentence)/2)-k):
			base = base[:i+1]+"-"+base[i+2:]
			base = base[:i+2]+char+base[i+3:]
			sys.stdout.write("\r"+base)
			sys.stdout.flush()
			time.sleep(0.001*(1+int((k+1)**(1/2.0))))
	time.sleep(0.7)
	for i in range(length*2):
		for j in range(i+1):
			base = base[:length-j]+" "+base[length-j:-1]
			sys.stdout.write("\r"+base)
			sys.stdout.flush()
			time.sleep(0.0015/int(1+(i**1.2)*0.1))
	time.sleep(0.3)
	sys.stdout.write("\r"*length)
		
def show_logo_random_fade():
	length = 120
	sentence = "UTab for PDA ver2.5"
	base = "-"*length
	for k, char in enumerate(reversed(sentence)):
		for i in range(int(length/2)+int(len(sentence)/2)-k):
			base = base[:i+1]+"-"+base[i+2:]
			base = base[:i+2]+char+base[i+3:]
			sys.stdout.write("\r"+base)
			sys.stdout.flush()
			time.sleep(0.001*(1+int((k+1)**(1/2.0))))
	time.sleep(0.7)
	numbers = [i for i in range(length)]
	random.shuffle(numbers)
	for i in range(length):
		n = numbers[i]
		base = base[:n+1]+" "+base[n+2:]
		sys.stdout.write("\r"+base)
		sys.stdout.flush()
		time.sleep(0.004)
	time.sleep(0.7)

	sys.stdout.write("\r"*length)

def progress_bar():
	END = 170
	for i in range(END+1):
		time.sleep(0.01)
		progress = 1.0 * i / END
		sys.stderr.write('\r\033[K' + get_progressbar_str(progress))
		sys.stderr.flush()
	sys.stderr.write('\n')
	sys.stderr.flush()
	time.sleep(0.7)