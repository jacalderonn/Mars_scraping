from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def scrape():
    ######## JPL Mars Space Images - Featured Image ########
    # URL of page to be scraped
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    response_news = requests.get(news_url)
    soup_news = bs(response_news.text, "html.parser")

    results_news = soup_news.find_all("div", class_ = "slide")

    mars_info = []
    # loop over results to get news data
    for result in results_news:
        # scrape the article title and the paragraph
        news_title = result.find('div', class_='content_title').text    
        news_p = result.find('div', class_='rollover_description_inner').text

        # Dictionary to be inserted
        post = {
            "title": news_title,
            "paragraph": news_p
        }
        
        # Inserting into a dictionary
        mars_info.append(post)
    
    news_len = len(mars_info)

    ######## JPL Mars Space Images - Featured Image ########
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

    browser = Browser("chrome", **executable_path, headless = False)
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")

    html_image = browser.html
    soup_image = bs(html_image, "lxml")
    image = soup_image.find_all("img", class_ = "main_image")
    src = image[0]["src"]

    #URL of the largest size featured image
    base_url_img = "https://www.jpl.nasa.gov"
    featured_image_url = base_url_img + src

    mars_info.append(featured_image_url)

    ######## Mars Facts ########
    url = "https://space-facts.com/mars/"
    
    tables = pd.read_html(url)
    data_table = tables[0]

    data_table.to_html("fact_table.html", index = False)

    ######## Mars Hemispheres ########
    # URL's 
    base_url = "https://astrogeology.usgs.gov"
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    response = requests.get(hemis_url)
    soup = bs(response.text, "html.parser")

    # Getting the links of each image
    image_url = []
    images = soup.find_all("a", class_ = "itemLink product-item")

    for link in images:
        image_url.append(link.get('href'))

    # Array to store names and the url's of each hemisphere
    hemisphere_image_urls = []

    # Getting the name and url's of the four images
    for i in range(len(images)):
        page_2 = base_url + image_url[i]
        
        # Going to the image webpage
        response_2 = requests.get(page_2)
        soup_2 = bs(response_2.text, "html.parser")
        
        # Getting the name of each hemisphere
        name = soup_2.find("h2").text
        name = name.rsplit(' ', 1)[0]
        
        # Getting the image url
        image_url_2 = soup_2.find("img", class_ = "wide-image")
        full_image_url = base_url + image_url_2["src"]
        
        # Storing the dictionary of name and link in an array
        temp_dict = {"name": name, "link": full_image_url}
        hemisphere_image_urls.append(temp_dict)
    
    mars_info.append(hemisphere_image_urls)
    
    print(mars_info)
    
    browser.quit()
    return mars_info