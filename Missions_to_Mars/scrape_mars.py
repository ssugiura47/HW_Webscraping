from bs4 import BeautifulSoup
from splinter import Browser
import re
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    Browser = init_browser()
    
# NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    Browser.visit(url)
    time.sleep(10)

    html = Browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    article = soup.select_one('ul.item_list li.slide')
    title = article.find('div', class_="content_title").text
    summary = article.find('div', class_="article_teaser_body").text
        
# JPL Mars Space Images
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    Browser.visit(featured_image_url)
    time.sleep(10)

    image_html = Browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    base_url = 'https://www.jpl.nasa.gov'

    featured_image_url = image_soup.find('img', class_ = 'thumb')['src']
    featured_image = base_url + featured_image_url

# Mars Weather
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    Browser.visit(mars_twitter_url)
    time.sleep(3)

    twitter_html = Browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
    time.sleep(3)

    tweets = twitter_soup.find_all("span",text=re.compile('InSight sol'))
    time.sleep(3)

    tweet = tweets[0].get_text() 

# Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    Browser.visit(mars_facts_url)

    mars_table = pd.read_html(mars_facts_url)[0]
    mars_table.columns =['Description', 'Value'] 
    mars_table = mars_table.set_index('Description')
    mars_table_html = mars_table.to_html()

# Mars Hemispheres
    mars_hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    Browser.visit(mars_hemis_url)
    time.sleep(10)

    mars_hemis_html = Browser.html
    mars_hemis_soup = BeautifulSoup(mars_hemis_html, 'html.parser')

    mars_hemis = mars_hemis_soup.find_all('div', class_='item')

    hemi_main_url = 'https://astrogeology.usgs.gov'
    hemis_image_urls = []

    for mars_hemi in mars_hemis:
        mars_hemis_title = mars_hemi.find('h3').text
        img_urls = hemi_main_url + mars_hemis_soup.find('img', class_='thumb')['src']
        hemis_image_urls.append({'title': mars_hemis_title, 'img_urls': img_urls})

    mars_info = {
        "news_title": title,
        "news_summary": summary,
        "featured_image": featured_image,
        "weather": tweet,
        "mars_facts": mars_table_html,
        "hemispheres": hemis_image_urls
    }

    # Close the browser after scraping
    Browser.quit()

    # Return results
    return mars_info