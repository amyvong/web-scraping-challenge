import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)



def scrape_info():
    browser = init_browser()
    article_t, article_p = article_title(browser)
    data={
        'article_t': article_t,
        'article_p': article_p,
        'featured_image_url' : feat_img(browser),
        'mars_facts': mars_facts(),
        'hemispheres' : hemispheres(browser)
    }
    browser.quit()
    return data
    


def article_title(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(1)
    slides=soup.select_one('ul.item_list li.slide')

    article_t = slides.find('div', class_='content_title').a.text

    article_p = slides.find('div', class_='article_teaser_body').text

    return article_t, article_p


def feat_img(browser):
    url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    feat_image = soup.find('figure', class_='lede').a['href']
    featured_image_url ='https://www.jpl.nasa.gov' + feat_image
    return featured_image_url


def mars_facts():
    url = 'https://space-facts.com/mars/'
    marsfacts=pd.read_html(url)[0]
    marsfacts.columns=['description', 'data']
    marsfacts.set_index('description', inplace =True)  
    return marsfacts.to_html() 



def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # html = browser.html
    # soup = bs(html, 'html.parser')
    hems_class=browser.find_by_css('.description')

    hems_url=[]
    for hems in range(len(hems_class)):
        hemispheres_info={}
        hems_titles=browser.find_by_tag('h3')[hems].text
        browser.find_by_tag('h3')[hems].click()
        hems_img=browser.find_by_text('Sample').first['href']
        hemispheres_info['title']=hems_titles
        hemispheres_info['image']=hems_img
        hems_url.append(hemispheres_info)
    return hems_url
  

