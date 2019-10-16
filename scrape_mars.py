## Import libraries #####################################################
from splinter import Browser
from bs4 import BeautifulSoup
from flask import Flask, render_template
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\\fireh\\Chome_Driver\\chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


def scrape():
### NASA MARS NEWS #####################################################
    browser = init_browser()
    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

# Sweep web page
    articles = soup.find_all('div', class_='list_text')
    headlines = soup.find_all('div', class_='content_title')
    paragraphs = soup.find_all('div', class_='article_teaser_body')

    headline = []
    paragraph = []
    for article in articles:
        headline.append(article.find(class_="content_title").text)
        paragraph.append(article.find(class_="article_teaser_body").text)
        #print('**HEADLINE**: ', headline)
        #print('**PARAGRAPH**: ',paragraph)
        time.sleep(0.5)



### MARS IMAGES #####################################################
    image_url = 'https://www.jpl.nasa.gov'
    query = '/spaceimages/?search=&category=Mars'
    site = image_url + query
    browser.visit(site)
    time.sleep(2)

# Scrape link from "Class = button_fancybook"
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'lxml')

# Output
    mars_image = image_soup.find(class_='button fancybox')

#Use .get() function to scrape the data-fancybox-href content
    image_link = mars_image.get('data-fancybox-href')
    site_link = image_url + image_link
    #print(site_link)



### MARS WEATHER #####################################################
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)

# Scrape link from "Class = button_fancybook"
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'lxml')

# Output Mars Weather
    mars_weather = weather_soup.find(class_='js-tweet-text-container').text
    #print(mars_weather)


    
### MARS FACTS #####################################################
    import pandas as pd

# Scrape tables using Pandas
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)

#Mars Comps HTML output table
    mars_comps_table = facts_table[0].to_html(index=False)
    #print(mars_comps_table)



### MARS HEMISPHERES ###############################################
    astrogeology_url = 'https://astrogeology.usgs.gov'
    query_url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_url = astrogeology_url + query_url
    browser.visit(hemi_url)
    time.sleep(2)

# Scrape image url directories into "hemi_images"
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'lxml')

    hemisphere_info = hemi_soup.find_all('div', {'class': 'item'})

    hemi_images=[]
    hemi_titles=[]
    for info in hemisphere_info:
        images = info.find('a',{'class': 'itemLink product-item'}).get('href')
        titles = info.find('h3').text

        hemi_images.append(images)
        hemi_titles.append(titles)
    
# Scrape image source files 

    img_url=[]
    for image in hemi_images:
        link_url = astrogeology_url + image
        browser.visit(link_url)
        link_html = browser.html
        time.sleep(0.5)

        image_soup = BeautifulSoup(link_html, 'lxml')
        image_info = image_soup.find('a',{'target': '_blank'}).get('href')
        img_url.append(image_info)

#Scrape the Hemisphere titles
    img_title=[]
    for title in hemi_titles:
        t=title.split(' ', 2)
        img_title.append(t[0])

#Output Files are lists: img_url and img_title
    #print(img_url)
    #print(img_title)


### CREATE MARS DICTIONARY ###############################################
    mars_dict = {'mars_headlines': headline,
                'mars_paragraphs': paragraph,
                'mars_image': site_link,
                'mars_weather': mars_weather,
                'mars_facts': mars_comps_table, 
                'mars_hemi_images': img_url,
                'mars_hemi_titles': img_title
                }
    
    browser.quit()

    return mars_dict