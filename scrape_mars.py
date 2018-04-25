# Dependencies
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
import tweepy
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', **executable_path, headless=False)

# Define scrape
def Scrape():
	mars ={}

	#Visit NASA Mars News
	url = "https://mars.nasa.gov/news/"
	browser.visit(url)
	html = browser.html
	soup = bs(html, 'html.parser')

	# Find the latest Mars news.
	news_p = article.find("div", class_="article_teaser_body").text
	news_title = article.find("div", class_="content_title").text
	news_date = article.find("div", class_="list_date").text

	# Add the news date, title and summary to the dictionary
	mars["news_date"] = news_date
	mars["news_title"] = news_title
	mars["summary"] = news_p


	# JPL's Featured Space Image
	url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url2)
	html = browser.html
	soup = bs(html, 'html.parser')
	image = soup.find('img', class_="thumb")["src"]
	img_url = "https://jpl.nasa.gov"+image
	featured_image_url = img_url

	# Add the featured image url to the dictionary
	mars["featured_image_url"] = featured_image_url


	# Visit the Mars Weather twitter account
	# Twitter API Keys
	consumer_key = "eTtvLod8ciVLik2M4DX1e2es7"
	consumer_secret = "sP0xw8vzk2Y2fZ9ElvuC8F2u3r8Ec6eA3y5n1sGXMuaR2YhVnP"
	access_token = "938583684415918080-dT5Oz9YL68meddX9k32DIB8Tvq7oUiD"
	access_token_secret = "ozqAYDE9KmVzaf5oRPEAnWEhOS01sxpHnFc01c0l0cy0k"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
	target_user = "marswxreport"
	full_tweet = api.user_timeline(target_user , count = 1)
	mars_weather=full_tweet[0]['text']

	# Add the weather to the dictionary
	mars["mars_weather"] = mars_weather

	# Mars Facts



	url3 = "https://space-facts.com/mars/"
	browser.visit(url3)

	table=pd.read_html(url3)
	mars_facts=pd.DataFrame(table[0])
	mars_facts.columns=['Mars','Data']
	mars_table=mars_info.set_index("Mars")
	marsdata=mars_table.to_html(classes='marsdata')
	marsdata =marsdata.replace('\n', ' ')

	# Add the Mars facts table to the dictionary
	mars["mars_table"] = marsdata


	# Visit the USGS Astogeology site
	url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url4)
	html = browser.html
	soup = bs(html, 'html.parser')
	mars_hemis=[]

	for i in range (4):
	time.sleep(5)
	images = browser.find_by_tag('h3')
	images[i].click()
	html = browser.html
	soup = bs(html, 'html.parser')
	image = soup.find("img", class_="wide-image")["src"]
	img_title = soup.find("h2",class_="title").text
	img_url = 'https://astrogeology.usgs.gov'+ image
	dictionary={"title":img_title,"img_url":img_url}
	mars_hemis.append(dictionary)
	browser.back()

	mars['mars_hemisphere'] = mars_hemis
	# Return the dictionary
	return mars
