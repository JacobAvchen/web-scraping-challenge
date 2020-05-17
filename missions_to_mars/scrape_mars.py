import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import re
import time


def scrape():

    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    info_url = "https://space-facts.com/mars/"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    mars_data = {}

    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path)

    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    titles = soup.find_all('div', class_='content_title')
    paras = soup.find_all('div', class_='article_teaser_body')
    mars_data['first_title'] = titles[1].text
    mars_data['first_para'] = paras[0].text

    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    images = soup.find_all('article', class_='carousel_item')
    mars_data['featured_image'] = "https://www.jpl.nasa.gov" + images[0].find('a')['data-fancybox-href']

    browser.visit(twitter_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    pattern = re.compile('InSight')
    tweets = soup.find_all(text=pattern)
    mars_data['weather'] = tweets[0]

    tables = pd.read_html(info_url)
    mars_df = tables[0]
    mars_df.columns = ['Category', 'Value']
    mars_df.set_index('Category')
    html_table = mars_df.to_html()
    html_table.replace('\n', '')
    mars_data['table'] = html_table

    browser.visit(hemisphere_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_titles = soup.find_all('div', class_='description')
    hemisphere_info = []

    for title in hemisphere_titles:
        hemisphere_info.append({'title': title.find('h3').text})
        for item in hemisphere_info:
            item['title'] = item['title'].replace(' Enhanced', '')
    
    for item in hemisphere_info:
        browser.visit(hemisphere_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        browser.click_link_by_partial_text(item['title'])
        html = browser.html
        soup = bs(html, 'html.parser')
        hemisphere_pics = soup.find_all('div', class_='downloads')
        item['img_url'] = hemisphere_pics[0].find('a')['href']
    
    mars_data['hemisphere_pics'] = hemisphere_info
    browser.quit()
    return mars_data