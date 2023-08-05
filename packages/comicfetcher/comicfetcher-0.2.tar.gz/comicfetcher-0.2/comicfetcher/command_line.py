import requests
from bs4 import BeautifulSoup
import datetime
import re
import six

if six.PY2:
    from urllib2 import urlretrieve
    from urllib2 import quote
    input = raw_input
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlretrieve

FILE_TYPE = '.png'

def main():
	explosm()

def explosm():
	find = re.compile( r'.+?(?=' + re.escape(FILE_TYPE) + r')' )
	now = datetime.datetime.now()
	date = str(now.day)+'-'+str(now.month)+'-'+str(now.year) 
	response = requests.get('http://explosm.net/')
	soup = BeautifulSoup(response.text, 'html.parser')
	comic_src = soup.find('img', {'id' : 'featured-comic'}).get('src')

	found = re.match(find,comic_src).group()	
	comic_url = 'http:'+found+FILE_TYPE
	file_name = date + ' ' + found.split('/')[-1]
	urlretrieve(comic_url, file_name + FILE_TYPE)
	print('Saved %s'%(found.split('/')[-1]))