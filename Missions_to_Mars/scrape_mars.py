from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():

    browser=init_browser()
    mars_dict={}

    # Visit redplanetscience.com
    nasa_url = "https://redplanetscience.com/"
    browser.visit(nasa_url)
        
    # Scrape page into Soup
    nasa_html = browser.html
    soup = bs(nasa_html, "html.parser")

    # Get the titles
    titles = soup.find_all('div', class_='content_title')[0].text

    # Get the paragraphs
    paras = soup.find_all('div', class_='article_teaser_body')[0].text


    # Store data in a dictionary
    mars_data = {
            "titles": titles,
            "paras": paras
        }

    mars_data

    

    # Visit spaceimages-mars.com
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)
        
    # Scrape page into Soup
    jpl_html = browser.html
    soup = bs(jpl_html, "html.parser")


    links_with_text = []
    for a in soup.find_all('a', href=True): 
        if a.text: 
            links_with_text.append(a['href'])
    #links_with_text
    featured_image_url =jpl_url +links_with_text[2]
    featured_image_url

    

    mars_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(mars_url)
    fact_table = tables[1]
    fact_table

    facts=fact_table.to_html()
    facts

    facts.replace('\n','')
    

    

    # Visit marshemispheres.com
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
        
    # Scrape page into Soup
    hemi_html = browser.html
    soup = bs(hemi_html, "html.parser")


    # Extract hemispheres item elements
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]



    # Loop through each hemisphere item
    for item in mars_item:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(hemi_url+hem_url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                # Print results
                print('-'*50)
                print(title)
                full = hemi_url+image_src
                print(full)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':full
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)

    mars_dict={
        "titles": titles,
        "paras": paras,
        "featured_image_url":featured_image_url,
        "fact_table":facts,
        "hemisphere_images":hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
    return mars_dict

