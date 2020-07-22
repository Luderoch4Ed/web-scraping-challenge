from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_text = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_text,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": weather(browser),
        "facts": facts(),
        "date_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    # NASA Mars News Site
    nasamars_url = ('https://mars.nasa.gov/news/')
    browser.visit(nasamars_url)
    # time.sleep(2)
    html = browser.html
    #soup = BeautifulSoup(html, 'html.parser')
    # soup = BeautifulSoup(html, 'lxml')

    
    nasa_news = browser.find_by_css("ul.item_list li.slide").first
    # print("Title: ",nasa_news.find_by_css("div.content_title").text)
    # print("Body: ",nasa_news.find_by_css("div.article_teaser_body").text)
    news_title = nasa_news.find_by_css("div.content_title").text
    news_text = nasa_news.find_by_css("div.article_teaser_body").text
    #news_title = nasa_news.find("div", class_='content_title').get_text()
    #news_text = nasa_news.find("div", class_='article_teaser_body').get_text()
    # news_title = soup.find('div', class_='bottom_gradient').text
  
    # Get news text 
    # news_text = soup.find('div', class_='article_teaser_body').text
    
    return news_title, news_text

def featured_image(browser):
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # locate full image and click on it
    full_image = browser.find_by_id("full_image")
    full_image.click()

    # locate 'more info' and click on it
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info= browser.find_link_by_partial_text("more info")
    more_info.click()

    # parse the html using BeautifulSoup
    img_bs= BeautifulSoup(browser.html, "html.parser")

    image_url = img_bs.select_one('figure.lede a img').get("src")

    # build complete url 
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    return featured_image_url
   


def hemispheres(brovwser):
    browser.visit("https://astrogeology.usgs.go/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):

        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()

        hemi_data = scrape_hemisphere(browser.html)

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)

        # Return to prior location
        browser.back()

    return hemisphere_image_urls

 
def weather(browser):
    browser.visit('https://twitter.com/marswxreport?lang=en')
    return browser.find_by_css("Article div[lang='en']").first.text
    #mars_weather = [ tw.text  for tw in browser.find_by_css("Article div[lang='en']") ]

    # get the most current tweet data
  
    #return mars_weather[0]


def scrape_hemisphere(html_text):

    # Soupify the html text
    hemi_soup = BeautifulSoup(html_text, "html.parser")

    # Try to get href and text except if error.
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:

        # Image error returns None for better front-end handling
        title_elem = None
        sample_elem = None

    hemisphere = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemisphere


def facts():
    tables = pd.read_html('http://space-facts.com/mars/')
    table_df = tables[0]
    table_df.columns = ['Parameter','Mars']
    table_df.to_html('mars_facts.html', index=False)
    table_df.set_index('Parameter')
    mars_facts = table_df.to_html(classes="table table-striped")
    
    return mars_facts


if __name__ == "__main__":
    print(scrape())