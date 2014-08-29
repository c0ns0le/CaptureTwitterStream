# Link Scrappers
# Each function expects a body of HTML, returns a tuple ({Title}, {Body Text})
import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata

# GetHTML returns the HTML of a resolved URL
def GetHTML(startingURL):
	r = requests.get(startingURL)
	#with open('file.html', 'w') as f:
		#f.write(r.text.encode("UTF-8"))
	return r.text

# For use with the bs4 function find_all()
# Grabs all paragraphs in the soup w/o an ID attribute
def paragraph_with_no_id(tag):
    return (not tag.has_attr('id') and (tag.name == 'p'))
	

#@NBCNews
def NBCNews(html):
	# Try, and if any errors, just return (None, None)
	# This may not be the most elegant, but with lots of data, we can probably afford to lose some data
	try:
		soup = BeautifulSoup(html)
	
		# the only <h1> tag contains the report Title
		title = soup.find_all('h1')[0].string
	
		# Grabs every <p> tag, and combines the plain-text of them together into one long string of text
		text = ' '.join([x.get_text() for x in soup.find_all('p')])
	
		if title != "" and text != "": return (title, text)
	
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	
	except:
		return (None, None)


#@MarketWatch
# MarketWatch tweets links to different styles of journalism (slideshows, reports, etc).
# This function distingushes between a MW Story and a MW Blog post, handling each one.
def MarketWatch(html):
	# Try, and if any errors, just return (None, None)
	# This may not be the most elegant, but with lots of data, we can probably afford to lose some data
	try:
		soup = BeautifulSoup(html)
	
		# If it is a story...
		if len(soup.find_all('article')) != 0:
				# title = {Main Title} - {Subtitle}
				title = soup.find_all('h1')[0].string + " - " + soup.find_all('h2')[0].string
	
				# make another soup from the article
				article = unicode(soup.find_all('article')[0])
				soup2 = BeautifulSoup(article)
	
				# Exchange newlines for whitespace
				text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all('p')])
	
				if title != "" and text != "": return (title, text)
		
		else:
			title = soup.find_all('h1')[0].string
		
			# make another soup from the article
			article = unicode(soup.find_all(class_='articlePage')[0])
			soup2 = BeautifulSoup(article)
	
			# Exchange newlines for whitespace
			text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all('p')])
		
			if title != "" and text != "": return (title, text)
	
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
		
	except:
		return (None, None)


# YahooFinance
def YahooFinance(html):
	# Try, and if any errors, just return (None, None)
	# This may not be the most elegant, but with lots of data, we can probably afford to lose some data
	try:
		soup = BeautifulSoup(html)
	
		# May be multiple H1s, but the pattern is discernable
		possibleTitles = soup.find_all('h1')
		if len(possibleTitles) == 1:
			title = soup.find_all('h1')[0].string
		elif len(possibleTitles) == 2:
			title = soup.find_all('h1')[1].string
			
		# make another soup from the article
		article = unicode(soup.find_all(class_='body yom-art-content clearfix')[0])
		soup2 = BeautifulSoup(article)
		
		# Exchange newlines for whitespace
		text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all('p')])
		
		if title != "" and text != "": return (title, text)
	
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	except:
		return (None, None)
		
		
# GoogleFinSvcs
# They link to many disparate sources; no pattern; no usable data
def GoogleFinSvcs(html):
	try:
		return (None, None)
	except:
		return (None, None)


# CNN
def CNN(html):
	try:
		soup = BeautifulSoup(html)
	
		# the only <h1> tag contains the report Title
		title = soup.find_all('h1')[0].string
		
		
		# make another soup from the article
		article = unicode(soup.find_all(class_='cnn_strycntntlft')[0])
		soup2 = BeautifulSoup(article)
		
		# Grabs every <p> tag, and combines the plain-text of them together into one long string of text
		text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all(paragraph_with_no_id)])
		
		
		if title != "" and text != "": return (title, text)
		
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	except:
		return (None, None)


# CNNMoney
# There are multiple possible layouts for a link from CNNMoney
def CNNMoney(html):
	try:
		soup = BeautifulSoup(html)
	
		# the only <h1> tag contains the report Title
		# The Title is consitent across pages
		title = soup.find_all('h1')[0].string
		
		# one formatting
		if len(soup.find_all(id='storycontent')) > 0:
		
			# make another soup from the article
			article = unicode(soup.find_all(id='storycontent')[0])
			soup2 = BeautifulSoup(article)
		
			# Grabs every <p> tag, and combines the plain-text of them together into one long string of text
			text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all(paragraph_with_no_id)])
		
			if title != "" and text != "": return (title, text)
		
			
		# Another possible layout (slideshow, but we only grab the first slide)
		elif len(soup.find_all(id='slidebody')) > 0:
			
			# make another soup from the article
			article = unicode(soup.find_all(id='slidebody')[0])
			soup2 = BeautifulSoup(article)
		
			# Grabs every <p> tag, and combines the plain-text of them together into one long string of text
			text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all(paragraph_with_no_id)])
		
			if title != "" and text != "": return (title, text)
		
		
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	except:
		return (None, None)
		
		
# TheStreet
# TheStreet occasionally displays ads before the report. When this happens, this will return (None, None)
def TheStreet(html):
	try:
		soup = BeautifulSoup(html)
	
		# the only <h1> tag contains the report Title
		title = soup.find_all('h1')[0].string
		
		
		# make another soup from the article
		article = unicode(soup.find_all(class_='virtualpage')[0])
		soup2 = BeautifulSoup(article)
	
		# Grabs every <p> tag, and combines the plain-text of them together into one long string of text
		text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all(paragraph_with_no_id)])
	
	
		if title != "" and text != "": return (title, text)
		
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	except:
		return (None, None)
		
		
# Reuters
def Reuters(html):
	try:
		soup = BeautifulSoup(html)
	
		# the only <h1> tag contains the report Title
		title = soup.find_all('h1')[0].string
		
		
		# make another soup from the article
		article = unicode(soup.find_all(id='articleText')[0])
		soup2 = BeautifulSoup(article)
		
		# Grabs every <p> tag w/o an ID, and combines the plain-text of them together into one long string of text
		text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all(paragraph_with_no_id)])
		
		
		if title != "" and text != "": return (title, text)
		
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	except:
		return (None, None)
		
		
# ReutersBiz
# Identical to @Reuters
def ReutersBiz(html):
	try:
		return Reuters(html)
	except:
		return (None, None)


# FederalReserve
def FederalReserve(html):
	try:
		soup = BeautifulSoup(html)
	
		# grab the title, split it to get interesting info
		title = unicode(soup.title).split("--")[1]
		
		# make another soup from the article
		article = unicode(soup.find_all(id='leftText')[0])
		soup2 = BeautifulSoup(article)
		
		# Grabs every <p> tag w/o an ID, and combines the plain-text of them together into one long string of text
		text = ' '.join([x.get_text().replace('\r\n', ' ').replace('\n', ' ') for x in soup2.find_all(paragraph_with_no_id)])
		
		if title != "" and text != "": return (title, text)
		
		# Return the equivalent of NULL if we didn't get anything
		return (None, None)
	except:
		return (None, None)


# # Tests # #
#NBCNews
'''print NBCNews(GetHTML("http://t.co/0wNYlZGs3T"))'''

#MarketWatch
'''print MarketWatch(GetHTML("http://t.co/Q503bwPyOF"))	#This one should end up being ingored (None, None)
print MarketWatch(GetHTML("http://t.co/NSjWnwKrJZ"))	#This is a list of stories and should be ignored (None, None)
print MarketWatch(GetHTML("http://t.co/9j0mSYlPRm"))	#Blog post; will give us title and text
print MarketWatch(GetHTML("http://t.co/nkmHAqR1X2"))	#A news story; will give us title and text'''

#YahooFinance
'''print YahooFinance(GetHTML("http://t.co/MwyMa83sWA"))
print YahooFinance(GetHTML("http://t.co/BCOCcABJYz"))
print YahooFinance(GetHTML("http://t.co/vmN7CEdRdY"))
print YahooFinance(GetHTML("http://t.co/zBLENnGCPK"))'''

#GoogleFinSvcs
'''print GoogleFinSvcs(GetHTML("http://t.co/SI4shzc8"))
print GoogleFinSvcs(GetHTML("http://t.co/a85k13m"))
print GoogleFinSvcs(GetHTML("http://ow.ly/5L8mc"))
print GoogleFinSvcs(GetHTML("http://ow.ly/5Hk0F"))
print GoogleFinSvcs(GetHTML("http://ow.ly/5nYts"))
print GoogleFinSvcs(GetHTML("http://ow.ly/5iqCj"))
print GoogleFinSvcs(GetHTML("http://ow.ly/5c4yh"))
print GoogleFinSvcs(GetHTML("http://ow.ly/54sGN"))
print GoogleFinSvcs(GetHTML("http://ow.ly/53YmM"))'''

#CNN
'''print CNN(GetHTML("http://t.co/otxU0TsaPs"))
print CNN(GetHTML("http://t.co/noPapvCs1O"))
print CNN(GetHTML("http://t.co/2hlp0MuuOh"))
print CNN(GetHTML("http://t.co/nqbsOfa8Yd"))'''

#CNNMoney
'''print CNNMoney(GetHTML("http://t.co/pnLlifMs1E"))
print CNNMoney(GetHTML("http://t.co/jJgxXkCzCu"))
print CNNMoney(GetHTML("http://t.co/taKRRXUTlS"))
print CNNMoney(GetHTML("http://t.co/6agAHboUSE"))
print CNNMoney(GetHTML("http://t.co/RJq7g4mApD"))	#this is a picture, should return (None, None)'''

#TheStreet
'''print TheStreet(GetHTML("http://t.co/tNzx85nMav"))
print TheStreet(GetHTML("http://t.co/NpTCjlwazv"))
print TheStreet(GetHTML("http://t.co/3fUuZwv6NF"))'''

#Reuters
'''print Reuters(GetHTML("http://t.co/DWKhu4mJ0E"))
print Reuters(GetHTML("http://t.co/nvTGCUawXG"))
print Reuters(GetHTML("http://t.co/YgN6t8C95r"))
print Reuters(GetHTML("http://t.co/nfVARFqZjp"))'''

#ReutersBiz
'''print ReutersBiz(GetHTML("http://t.co/3UEUoi5Akq"))
print ReutersBiz(GetHTML("http://t.co/eSLEerosep"))
print ReutersBiz(GetHTML("http://t.co/dDlZnJVoOt"))
print ReutersBiz(GetHTML("http://t.co/kfnKiAq8qz"))'''

#FederalReserve
'''print FederalReserve(GetHTML("http://t.co/kmAhdB12so"))
print FederalReserve(GetHTML("http://t.co/44lgJSShmL"))
print FederalReserve(GetHTML("http://t.co/ELuz4IdxjH"))		#Should return (None, None)
print FederalReserve(GetHTML("http://t.co/ENM2oHTZh3"))		#Should return (None, None)'''




