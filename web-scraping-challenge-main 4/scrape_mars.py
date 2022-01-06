from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_info():
    
    listings = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)  

    url_1 = "https://redplanetscience.com/"
    browser.visit(url_1)
    time.sleep(1)
    html = browser.html
    soup = bs(html,"html.parser")
    news_title = soup.find(class_="content_title").text
    news_p = soup.find(class_="article_teaser_body").text
    listings["news_title"] = news_title
    listings["news_p"] = news_p

    url_2 = "https://spaceimages-mars.com/"
    browser.visit(url_2)
    time.sleep(1)
    html = browser.html
    soup = bs(html,"html.parser")
    img = soup.find(class_="headerimage fade-in")["src"]
    featured_image_url = url_2+img
    listings["featured_image_url"] = featured_image_url

    url_3 = "https://galaxyfacts-mars.com/"
    browser.visit(url_3)
    time.sleep(1)
    html = browser.html
    soup = bs(html,"html.parser")
    tabels = pd.read_html(url_3, header=0)
    mars_planet_profile = tabels[0].to_html(index=False)
    listings["mars_planet_profile"] = mars_planet_profile

    url_4 = "https://marshemispheres.com/"
    browser.visit(url_4)
    time.sleep(1)
    html = browser.html
    soup = bs(html,"html.parser")
    thumbs = soup.find_all("div",class_="item")
    pages = []
    for t in thumbs:
        pages.append(url_4+t.find("a")["href"])
    hemisphere_image_urls = []
    for p in pages:
        browser.visit(p)
        html = browser.html
        soup = bs(html,"html.parser")
        div = soup.find(class_="downloads")
        ul = div.find("ul")
        img = ul.find("a")["href"]
        img_url = url_4 + img
        title = soup.find(class_="title").text
        hemisphere_image_urls.append({"title":title, "img_url":img_url})
    listings["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    
    return listings
