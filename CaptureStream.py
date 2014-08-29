# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CaptureStream.py
# Copyright 2014 Pat York and Thomas Avant
# CS 491H - Data Science Project: Twitter Sentiment and U.S. Markets
#
# This function acts as one part of our 'main' project. Specifically, it captures the stream sample.
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import the TwitterFunctions
from packages import TwitterFunctions as T
import sys, os

if len(sys.argv) != 3:
	print "Usage: CaptureStream.py {StreamNumber} {TestDisplay|TestCount|Capture}"

# Start the stream capture with StreamApp1
elif sys.argv[1] == '1':
	while True:		# Restart as soon as possible in the event of a dropped connection
		try:
			if sys.argv[2].lower() == 'testdisplay':
				print "TEST: Printing the metadata!"
				T.SampleStream(1, ['printMeta'])	#test by displaying the stream
				
			elif sys.argv[2].lower() == 'testcount':
				print "TEST: Printing the tweet count!"
				T.SampleStream(1, ['printCount'])	#test by displaying the count only
				
			elif sys.argv[2].lower() == 'capture':
				print "CAPTURE: Capturing the tweets!"
				T.SampleStream(1, ['printCount', 'csvMeta'], 'Data/Stream')	#capture
		except:
			pass
			
# Start the stream capture with StreamApp2 #TODO
elif sys.argv[1] == '2':
	while True:		# Restart as soon as possible in the event of a dropped connection
		try:
			if sys.argv[2].lower() == 'testdisplay':
				print "TEST: Printing the metadata!"
				T.SampleStream(2, ['printMeta'])	#test by displaying the stream
				
			elif sys.argv[2].lower() == 'testcount':
				print "TEST: Printing the tweet count!"
				T.SampleStream(2, ['printCount'])	#test by displaying the count only
				
			elif sys.argv[2].lower() == 'capture':
				print "CAPTURE: Capturing the tweets!"
				T.SampleStream(2, ['printCount', 'csvMeta'], 'Data/Stream')	#capture
		except:
			pass

