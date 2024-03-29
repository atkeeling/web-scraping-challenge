#!/usr/bin/env python
# coding: utf-8

#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import pandas as pd

executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_data = {}

# # News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    html_news = browser.html
    soup = bs(html_news, "html.parser")

    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_data["mars_news_title"] = news_title
    mars_data["mars_paragraph"] = news_paragraph

# # JPL Images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    html_image = browser.html
    soup = bs(html_image, "html.parser")

    image = soup.find("a", id="full_image")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    mars_data["mars_image"] = featured_image_url

# # Weather

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather

# # Facts

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    mars_tables = pd.read_html(facts_url)
    df_mars = pd.DataFrame(mars_tables[1])
    mars_facts_html = df_mars.to_html(header = False, index = False)
    mars_data["mars_facts"] = mars_facts_html

# # Hemispheres

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    html_hemispheres = browser.html
    soup = bs(html_hemispheres, "html.parser")

    mars_hemispheres = []

    hemispheres = soup.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemispheres.append({"title": title, "img_url": image_url})
    mars_data["mars_hemispheres"] = mars_hemispheres

    return mars_data