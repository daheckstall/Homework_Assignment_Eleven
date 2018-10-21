from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def scrape():
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(news_url)
    soup = bs(response.text, "html.parser")
    
    news_title = soup.find("div", class_="content_title").text
    
    news_p = soup.find("div", class_="rollover_description_inner").text

    executable_path = {'executable_path': "../../../Downloads/chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)
    time.sleep(5)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)

    browser.click_link_by_partial_text("more info")
    navigated_mars_image_url = browser.url

    mars_response = requests.get(navigated_mars_image_url)
    soup = bs(mars_response.text, "lxml")

    results = soup.find("figure", class_ = "lede")
    featured_image_url = f'https://www.jpl.nasa.gov/{results.a["href"]}'

    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    weather_html = browser.html
    weather_soup = bs(weather_html, "lxml")
    mars_weather = weather_soup.find("p", class_="tweet-text").text

    mars_facts_url = "http://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    mars_html_table = df_mars_facts.to_html()
    mars_html_table.replace("\n", "")

    usgs_base_url = "https://astrogeology.usgs.gov"
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Cerberus")
    cerberus_html = browser.html
    cerberus_soup = bs(cerberus_html, "lxml")
    cerberus_results = cerberus_soup.find("img", class_="wide-image")["src"]
    cerberus_url = usgs_base_url + cerberus_results

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Schiaparelli")
    schiaparelli_html = browser.html
    schiaparelli_soup = bs(schiaparelli_html, "lxml")
    schiaparelli_results = schiaparelli_soup.find("img", class_="wide-image")["src"]
    schiaparelli_url = usgs_base_url + schiaparelli_results

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Syrtis")
    syrtis_html = browser.html
    syrtis_soup = bs(syrtis_html, "lxml")
    syrtis_results = syrtis_soup.find("img", class_="wide-image")["src"]
    syrtis_url = usgs_base_url + syrtis_results

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Valles")
    valles_html = browser.html
    valles_soup = bs(valles_html, "lxml")
    valles_results = valles_soup.find("img", class_="wide-image")["src"]
    valles_url = usgs_base_url + valles_results

    mars_data = {}

    mars_data["news_title"] = news_title.strip()
    mars_data["news_paragraph"] = news_p.strip()
    mars_data["featured_image"] = featured_image_url
    mars_data["weather"] = mars_weather
    mars_data["mars_df"] = df_mars_facts
    mars_data["images"] = hemispheres_url

    return mars_data