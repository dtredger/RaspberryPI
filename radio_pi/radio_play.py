# TODO ------ rather than using os.fork, I'd prefer to simply run this in a screen and detach -----

import os
import sys
import subprocess
import re
import random
import threading
import time


fm_process = None
on_off = ["off", "on"]

frequency = 101.1
shuffle = False
repeat_all = True
merge_audio_in = False
play_stereo = True

# --- reset these for your own settings ---
MUSIC_DIRECTORY = "/500gb_hd/music"
PIFM_BINARY_LOCATION = "/root/radio_pi/pifm"

music_pipe_r,music_pipe_w = os.pipe()
microphone_pipe_r,microphone_pipe_w = os.pipe()

def main():
	daemonize()
	setup()
	files = build_file_list()
	if repeat_all == True:
		while(True):
			play_songs(files)
	else:
		play_songs(files)
	return 0


def build_file_list():
	file_list = []
	for root, folders, files in os.walk(MUSIC_DIRECTORY):
		folders.sort()
		files.sort()
		for filename in files:
			if re.search(".(aac|mp3|wav|flac|m4a|pls|m3u)$", filename) != None: 
				file_list.append(os.path.join(root, filename))
	return file_list


def play_songs(file_list):
	print("Playing songs to frequency ", str(frequency))
	print("Shuffle is " + on_off[shuffle])
	print("Repeat All is " + on_off[repeat_all])
	print("Stereo playback is " + on_off[play_stereo])

	if shuffle == True:
		random.shuffle(file_list)
	with open(os.devnull, "w") as dev_null:
		for filename in file_list:
			print("Playing ",filename)
			if re.search(".pls$", filename) != None:
				streamurl = parse_pls(filename, 1)
				if streamurl != None:
					print("streaming radio from " + streamurl)
					subprocess.call(["ffmpeg","-i",streamurl,"-f","s16le","-acodec","pcm_s16le","-ac", "2" if play_stereo else "1" ,"-ar","44100","-"],stdout=music_pipe_w, stderr=dev_null)
			elif re.search(".m3u$", filename) != None:
				streamurl = parse_m3u(filename, 1)
				if streamurl != None:
					print("streaming radio from " + streamurl)
					subprocess.call(["ffmpeg","-i",streamurl,"-f","s16le","-acodec","pcm_s16le","-ac", "2" if play_stereo else "1" ,"-ar","44100","-"],stdout=music_pipe_w, stderr=dev_null)
			else:
				subprocess.call(["ffmpeg","-i",filename,"-f","s16le","-acodec","pcm_s16le","-ac", "2" if play_stereo else "1" ,"-ar","44100","-"],stdout=music_pipe_w, stderr=dev_null)


def parse_pls(src, titleindex):
	# breaking up the pls file in separate strings
	lines = []
	with open( src, "r" ) as f:
		lines = f.readlines()

	# and parse the lines
	if lines != None:
		for line in lines:
			# search for the URI
			match = re.match( "^[ \\t]*file" + str(titleindex) + "[ \\t]*=[ \\t]*(.*$)", line, flags=re.IGNORECASE )
			if match != None:
				if match.group( 1 ) != None:
				# URI found, it's saved in the second match group
				# output the URI to the destination file
					return match.group( 1 )

	return None

def parse_m3u(src, titleindex):
	# create a list of strings, one per line in the source file
	lines = []
	searchindex = int(1)
	with open( src, "r" ) as f:
  		  lines = f.readlines()

	if lines != None:
		for line in lines:
		# search for the URI
			if '://' in line:
				if searchindex == titleindex:
					return line
				else:
					searchindex += 1

	return None


def daemonize():
	fpid=os.fork()
	if fpid!=0:
		sys.exit(0)


def setup():
	run_pifm()

# TODO ------ is it necessary to spawn off a separate process?? I'd prefer to simply run this in a screen and detach -----
def run_pifm(use_audio_in=False):
	global fm_process
	with open(os.devnull, "w") as dev_null:
		fm_process = subprocess.Popen([PIFM_BINARY_LOCATION,"-",str(frequency),"44100", "stereo" if play_stereo else "mono"], stdin=music_pipe_r, stdout=dev_null)



main()
