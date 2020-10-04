from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import re
import pandas as pd



def scrape():
    cd C:\Users\sakis
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
 
    article = soup.select_one('ul.item_list li.slide')
    title = article.find('div', class_="content_title").text
    summary = article.find('div', class_="article_teaser_body").text
    
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    browser.visit(featured_image_url)
    time.sleep(1)

    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = image_soup.find('img', class_ = 'thumb')['src']
    featured_image = base_url + featured_image_url

    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)
    time.sleep(10)

    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    tweets = twitter_soup.find_all("span",text=re.compile('InSight sol'))
    tweet = latestweather=tweets[0].get_text()

    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)

    mars_table = pd.read_html(mars_facts_url)[0]
    mars_table_html = mars_table.to_html()

    mars_data = {
        "news_title": title,
        "news_summary": summary,
        "featured_image": featured_image,
        "weather": tweet,
        "mars_facts": mars_table_html,
        # "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data