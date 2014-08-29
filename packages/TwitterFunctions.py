# Function List (High-, Mid-, Low-level)
#
# StreamHandle(handle)						# Stream tweets from a Handle as they happen (<10 min delay)
# StreamHandles(handles)					# Stream from a list of Handles (<10 min delay)
# StreamID(userID)							# Stream tweets from an ID as they happen (<10 min delay)
# SampleStream(howToOutput, fileName='')	# Stream the ENGLISH sample of the firehose; how=[print, printText, storeFull, storePartial] or any subset
# TrackTerms(listOfTerms, howToOutput)		# Track certain terms how=[print, printText, storeFull, storePartial] or any subset
#
# UserIdFromHandle(handle)					# Get the UserId from a Handle
# ParseTweet(tweet, how=['printText'])		# Handle a tweet (an object returned from the API) how=[print, printText, storeFull, storePartial]  or any subset


from TwitterAPI import TwitterAPI
import datetime
from threading import Thread
import sys, os


# # # # # OAuth data # # # # #
# Twitter App #1 - For use with TrackTerms
CONSUMER_KEY_Terms = 'ybGIhnu9GPWkzHOJem3Tow'
CONSUMER_SECRET_Terms = 'OUNNpa2Y0yymTQ9KssG5yAvsPc24AunKncLkW7dTBUs'
ACCESS_TOKEN_KEY_Terms = '46986295-4ar0e23athY6MIrQnuwZXawDkCanFykSCDSsc3W1C'
ACCESS_TOKEN_SECRET_Terms = 'A0yyNk3CjlMxQlm8fvAW80gT7xkGxthd94H1Dgz5ygtUe'

# Twitter App #2 - For use with TrackAccounts
CONSUMER_KEY_Accounts = 'iZfCW8TQp3AUHg2E9VqbeA'
CONSUMER_SECRET_Accounts = 'mQrEvmxdFdBqRlk9AwH7qBY6loEuBPpKvtScXU9DY'
ACCESS_TOKEN_KEY_Accounts = '46986295-uPi0iSmej81n6Y4KZ5i9ptqaHyClJmubmuTI8AV5D'
ACCESS_TOKEN_SECRET_Accounts = '7zdCjLs6mNYbbPHL0Z9G32qteEGSFZstCLQW1kZwiHsLJ'

# Twitter App #3 - for use with CaptureStream {1}
CONSUMER_KEY_Stream1 = '1UzKHIh9uy2dPTtawmsVtQ'
CONSUMER_SECRET_Stream1 = 'j9yocgy2fSyQyMTUjN7RPhftrdvh02T0VRRBbtSn4'
ACCESS_TOKEN_KEY_Stream1 = '46986295-LDTPmNorKc089QU3zQezCjB3DncbyNbvZZWelhfJh'
ACCESS_TOKEN_SECRET_Stream1 = 'i0U5i0KG4IUdQxbYtryDp1XUMKCOXfqNJpzM6XQHdWkF5'

# Twitter App #4 - for use with CaptureStream {2}
CONSUMER_KEY_Stream2 = 'CNB76YwivlAfLDsnGCUlig'
CONSUMER_SECRET_Stream2 = 'jzKKGt65tvkFUzPxzJxm0VEVL9276FCThuthWATYW4'
ACCESS_TOKEN_KEY_Stream2 = '46986295-H0Pqs21olui1RUlTrQieD4hl5YVEudJ3cvG3AHuXr'
ACCESS_TOKEN_SECRET_Stream2 = '5yfROJAJaRALnL2mMSPsulFwOSW9IioVp6dVorzrkCf3q'

terms_api = TwitterAPI(CONSUMER_KEY_Terms, CONSUMER_SECRET_Terms, ACCESS_TOKEN_KEY_Terms, ACCESS_TOKEN_SECRET_Terms)
accounts_api = TwitterAPI(CONSUMER_KEY_Accounts, CONSUMER_SECRET_Accounts, ACCESS_TOKEN_KEY_Accounts, ACCESS_TOKEN_SECRET_Accounts)
stream_api1 = TwitterAPI(CONSUMER_KEY_Stream1, CONSUMER_SECRET_Stream1, ACCESS_TOKEN_KEY_Stream1, ACCESS_TOKEN_SECRET_Stream1)
stream_api2 = TwitterAPI(CONSUMER_KEY_Stream2, CONSUMER_SECRET_Stream2, ACCESS_TOKEN_KEY_Stream2, ACCESS_TOKEN_SECRET_Stream2)
# # # # # # # # # # # # # # #



# # # Highlevel Functions # # #

# Stream tweets from a Handle as they happen (<10 min delay)
def StreamHandle(handle):
	
	# Get UserId from Handle
	userID = UserIdFromHandle(handle)
	
	if userID == None:
		print "Error retrieving handle"		#TODO: throw exception?
	else:
		print "Now Following %s {%s}" % (handle, userID)
		StreamFromId(userID)


# Stream tweets from an ID as they happen (<10 min delay)
def StreamID(userID):
	if userID == None:
		print "Error retrieving handle"		#TODO: throw exception?
	else:
		print "Now Following %s {%s}" % ('User', userID)
		StreamFromId(userID)


# Stream from a list of Handles (<10 min delay)
def StreamHandles(handles):
	# Start a streaming Thread for each userID
	threads = []
	for handle in handles:
		threads.append(Thread(target = StreamHandle, args = (handle, )))
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()

		
# Stream the ENGLISH sample of the firehose
def SampleStream(streamNumber, howToOutput, directory='Data/Stream'):
	outFile = os.path.join(directory, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv'))
	
	# A higher level display
	tweetCount = 0
	tweetCountHundred = 0
	tweetCountThousand = 0
	displayTweetCount = False
	if 'printCount' in howToOutput:
		displayTweetCount = True
	
	# Select the correct Twitter App to use
	if streamNumber == 1:
		r = stream_api1.request('statuses/sample')
	else:
		r = stream_api2.request('statuses/sample')
		
	# Parse each English item
	for item in r:
		if 'lang' in item:
			if item['lang'] == 'en':
			
				tweetCount += 1		#Increment Tweet count
				if tweetCount % 100 == 0 and displayTweetCount:		# If we want to display a count, and it's time
					tweetCount = 0
					tweetCountHundred += 1
					if(tweetCountHundred == 10):
						tweetCountHundred = 0
						tweetCountThousand += 1
					print "Captured Tweet Count: %i.%i thousand @ %s" % (tweetCountThousand, tweetCountHundred, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					
				ParseTweet(item, howToOutput, outFile)
			
# Track certain terms
# Each term in the list will be an OR
#	Insert an item with just a space to make an AND:
#		EX: ['you', 'me', 'this that'] -> 'you' OR 'me' OR 'this AND that'	
def TrackTerms(listOfTerms, howToOutput, directory='Data/Stream'):
	outFile = os.path.join(directory, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv'))
	
	# A higher level display
	tweetCount = 0
	tweetCountHundred = 0
	tweetCountThousand = 0
	displayTweetCount = False
	if 'printCount' in howToOutput:
		displayTweetCount = True
	
	trackTerms = ','.join(listOfTerms)		# Convert the list of words to track into a comma-separated string
	
	r = terms_api.request('statuses/filter', {'track':trackTerms})	# Start a track on the terms
	
	# Do something with each item
	for item in r:
		if 'lang' in item:
			if item['lang'] == 'en':
				
				tweetCount += 1		#Increment Tweet count
				if tweetCount % 100 == 0 and displayTweetCount:		# If we want to display a count, and it's time
					tweetCount = 0
					tweetCountHundred += 1
					if(tweetCountHundred == 10):
						tweetCountHundred = 0
						tweetCountThousand += 1
					print "Captured Tweet Count (with tracked terms): %i.%i thousand @ %s" % (tweetCountThousand, tweetCountHundred, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
					
				ParseTweet(item, howToOutput, outFile)

# # # # # # # # # # # # # # # #



# # # Midlevel Functions # # #

# Get the UserId from a Handle
def UserIdFromHandle(handle):
	try:
		r = accounts_api.request('users/lookup', {'screen_name':handle})
		for item in r:
			if('id' in item): return item['id']
			
		return None
	except:
		return None


# Start a stream from a UserID
def StreamFromId(userID):
	try:
		r = accounts_api.request('statuses/filter', {'follow':userID})
		for item in r:
			#if ('text' in item): print item['text']
			print item
	except:
		print "Error streaming"		#TODO


# Grab recent Tweets by UserID
def RecentTweetsByUserId(userID):
	r = accounts_api.request('statuses/user_timeline', {'user_id':userID})
	for item in r:
		if ('text' in item): print item['text']


# Grab recent Tweets by Handle
def RecentTweetsByHandle(handle):
	r = accounts_api.request('statuses/user_timeline', {'screen_name':handle})
	for item in r:
		if ('text' in item): print item['text']

# Handle a tweet (an object returned from the API)
#	Switch on the parameter with what we want to do with it
def ParseTweet(tweet, how=['printText'], filename=''):

	# Print the JSON object
	if 'print' in how:
		print tweet
		
	# Print the Text only
	elif 'printText' in how:
		if 'text' in tweet:
			print tweet['text']
			
	elif 'printMeta' in how:
		try:	# Try to print all interesting data, break if one of the fields doesn't exist
			print "%s	%s" % (tweet['created_at'], tweet['text'])
		except:
			print "Error in metadata"
	
	if 'csvMeta' in how:
		if filename == '':
			return		#TODO
		try:
			with open(filename, 'a') as f:
				f.write("%s|;|%s|;|%s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tweet['created_at'], tweet['text']))
		except:
			pass
	
	# TODO
	elif 'storeFull' in how:
		pass		# TODO storing
	elif 'storePartial' in how:
		pass		# TODO storing

# # # # # # # # # # # # # # #


# # # Tests # # #

#StreamHandle("drunkenFilosofr")			#working; 5-10min delay
#print UserIdFromHandle('drunkenFilosofr')	#working
#RecentTweetsByUserId('46986295')			#working
#RecentTweetsByHandle('drunkenFilosofr')	#working
#StreamHandles(['NBCNews', 'MarketWatch', 'YahooFinance', 'CNN', 'CNNMoney', 'TheStreet', 'Reuters', 'ReutersBiz', 'FederalReserve', 'fakeprogileadfasdf'])

#SampleStream(['printMeta'])					#working
#SampleStream(1, ['printCount', 'csvMeta'], 'streamData')


#WatchedStocks = 'SIRI,FB,CSCO,F,MSFT,PHOT,GE,MU,INTC,ARIA,JCP,AA,RAD,ZNGA,GM,BBRY,PFE,C,T,EMC,AMD,NOK,TWTR,PLUG,S,VALE,PBR,JPM,ORCL,YHOO,GRPN,WFC,VZ,KO,ABX,CX,RF,EBAY,HPQ,UNG,CMCSA,NLY,FNMA,MRK,AAPL,DAL,XOM,MS,XRX,FOXA,LSI,ANR,ALU,BSX,GILD,AMAT,GLW,MGM,DOW,SUNE,FCX,NEM,KEY,TSM,KGC,ITUB,VOD,HBAN,NRF,JNPR,QCOM,FTR,BBY,ODP,GALE,AIG,SD,ABEV,ACI,HAL,TSLA,MDLZ,PG,RNN,MO,CHK,P,VLO,HTZ,BMY,SPLS,GG,CLF,HIMX,CIM,JNJ,WMB,BBD,USB,MA,NVDA,BRCM,AUY,WFT,SNV,WEN,LUV,EXC,SYMC,FITB,ARCP,GGP,ATVI,DIS,AKS,X,PHM,NUAN,ABT,DHI,BTU,ABBV,WIN,IAG,TMUS,MCP,POT,YGE,WAG,WU,TGT,HST,SCHW,FMCC,HD,ONNN,MNKD,RFMD,WMT,NIHD,WLT,AGNC,LOW,TEVA,GTAT,CVX,CSX,TRTC,KMI,AES,FCEL,SLB,SAN,CAT,MRVL,MTG,JBLU,TXN,CTL,EA,PM,AMRN,CVS,FLEX,DDD,CHTP,SBUX,KOG,GERN,MET,SID,OIBR,UAL,EGO,COG,GNW,AMX,MT,HL,MRO,LLY,XCO,ARNA,MCD,DNR,GFI,SYY,GPS,HK,PEP,NVAX,CIG,LQMT,ARR,IBM,TWX,AEO,BSBR,IGT'
#ListOfStocks = WatchedStocks.split(',')
#TrackTerms(['$' + x for x in ListOfStocks], ['printText'])	# Watch our list of stocks, using ${STOCKSYMBOL} as the track term								

# # # # # # # # #


