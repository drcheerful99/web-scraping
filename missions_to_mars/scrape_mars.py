#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# url to be scraped
url = 'https://mars.nasa.gov/news/'
response = requests.get(url)


# In[3]:


# Create bs object and parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# In[4]:


# find div and class for loop
results = soup.find_all('div', class_="content_title")
results


# In[5]:


# create an empty list to hold the headlines
news_titles = []
# Loop through div elements
for result in results:
    # id the link anchor
    if (result.a):
        # check whether link has text...
        if (result.a.text):
            # if found, append text to the list
            news_titles.append(result)
news_titles


# In[6]:


# find only the headlines
headlines = []
for i in range(6):
    var=news_titles[i].text
    var = var.strip('\n\n')
    headlines.append(var)
headlines


# In[7]:


# find descriptive paragraph below title
paraResults = soup.find_all('div', class_='rollover_description_inner')
paraResults


# In[8]:


# loop thorugh div and pull out text
news_para = []
for i in range(6):
    var=paraResults[i].text
    var = var.strip('\n\n')
    news_para.append(var)
news_para


# In[9]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
print(soup.prettify())


# In[10]:


images = soup.find_all('a', class_='fancybox')
images


# In[11]:


# get image links
featured_image = []
for image in images:
    pic = image['data-fancybox-href']
    featured_image.append(picture)

featured_image_url = 'https://www.jpl.nasa.gov' + pic
featured_image_url


# In[ ]:


### Mars Facts

#* Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

#* Use Pandas to convert the data to a HTML table string.


# In[12]:


url = 'https://space-facts.com/mars/'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
print(soup.prettify())


# In[13]:


table = pd.read_html(url)
table [0]


# In[14]:


# make dataframe
mars_df = table[0]
mars_df


# In[15]:


mars_df.columns = ['Stats','Measurement']
mars_df.head()


# In[16]:


# formatting
s = pd.Series(mars_df['Stats'])
mars_df['Stats'] = s.str.strip(':')
mars_df


# In[17]:


# set index
mars_df = mars_df.set_index('Stats')
mars_df


# In[18]:


# generate table from dataframe
mars_table = mars_df.to_html('mars_table.html')


# In[ ]:


# ### Mars Hemispheres

# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.

# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# ```python
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
# ```


# In[21]:


# Setting up windows browser with chromedriver
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[22]:


# Setting url for different browser
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[23]:


nextpage_urls = []
imgtitles = []
base_url = 'https://astrogeology.usgs.gov'

# HTML object
html = browser.html
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')
# Retrieve all elements that contain hemisphere photo info
divs = soup.find_all('div', class_='description')

# Iterate through each div to pull titles and make list of hrefs to iterate through
counter = 0
for div in divs:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
    link = div.find('a')
    href=link['href']
    img_title = div.a.find('h3')
    img_title = img_title.text
    imgtitles.append(img_title)
    next_page = base_url + href
    nextpage_urls.append(next_page)
    counter = counter+1
    if (counter == 4):
        break
print(nextpage_urls)
print(imgtitles)


# In[24]:


# loop through for high res photo on next page

hires_images=[]
for nextpage_url in nextpage_urls:
    url = nextpage_url
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    link2 = soup.find('img', class_="wide-image")
    forfinal = link2['src']
    full_img = base_url + forfinal
    hires_images.append(full_img)
    nextpage_urls = []
hires_images


# In[25]:


# Creating  list of dictionaries
# key: imgurl and tile
# value: imagtitles and hires image

hemisphere_image_urls = []

cerberus = {'title':imgtitles[0], 'img_url': hires_images[0]}
schiaparelli = {'title':imgtitles[1], 'img_url': hires_images[1]}
syrtis = {'title':imgtitles[2], 'img_url': hires_images[2]}
valles = {'title':imgtitles[3], 'img_url': hires_images[3]}

hemisphere_image_urls = [cerberus, schiaparelli, syrtis, valles]
print(hemisphere_image_urls)

