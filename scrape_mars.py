from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests as req
import pandas as pd

    
#browser = init_browser()
def scrape():
    url = "https://mars.nasa.gov/news/"
    time.sleep(3)
    html = req.get(url)
    soup = bs(html.text, "html5lib")
    news_title = soup.find('div', class_="content_title").text
    #end title section
    news_p =soup.find('div',class_="rollover_description_inner").text
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    #paragraph
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    temp_img_url = new_soup.find('img', class_='main_image')
    back_half_img_url = temp_img_url.get('src')

    recent_mars_image_url = "https://www.jpl.nasa.gov" + back_half_img_url
    twitter=req.get("https://twitter.com/marswxreport?lang=en")
    mars_weather=bs(twitter.text, 'html.parser')
    twitter_html=mars_weather.find_all('div', class_="js-tweet-text-container")
    space_facts=req.get("http://space-facts.com/mars/")
    mars_df=pd.read_html(space_facts.text)
    df=mars_df[0]
    df_html=df.to_html()
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    astro_req = req.get(astro_url)
    soup = bs(astro_req.text, "html.parser")
    attrib= soup.find_all('a', class_="itemLink product-item")
    hemisphere_image = []
    for hemi_img in attrib:
        img_title = hemi_img.find('h3').text
        link_to_img = "https://astrogeology.usgs.gov/" + hemi_img['href']
        img_request = req.get(link_to_img)
        soup = bs(img_request.text, 'lxml')
        img_tag = soup.find('div', class_='downloads')
        img_url = img_tag.find('a')['href']
        hemisphere_image.append({"Title": img_title, "Image_Url": img_url})

    mars_data = {
        "News": news_title,
        "Paragraph_Text": news_p,
        "Most_Recent_Mars_Image": recent_mars_image_url,
        "Mars_Weather": mars_weather,
        "mars_h": hemisphere_image
        }
    return mars_data