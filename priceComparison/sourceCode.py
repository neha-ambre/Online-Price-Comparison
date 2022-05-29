##putting it all together
from bs4 import BeautifulSoup
import urllib

#firefox & chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

##getting the page
def get_amazon_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ','+')
    return template.format(search_term)

def get_flipkart_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
    search_term = search_term.replace(' ','+')
    return template.format(search_term)

##Generalize the pattern 
def extract_amazon_record(item):
    """Extract and return data from a single record"""
    #description and url
    atag = item.h2.a  # because it is the only h2 tag on the page
    description = atag.text.strip()  #name or title of the product
    prod_url = 'https://www.amazon.in' + atag.get('href')  #product link
    
    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        price =''
    
    #rank and rating
    try:
        rating=item.i.text
    except AttributeError:
        rating=''
    
    try:
        rating_cnt=item.find('span', {'class':'a-size-base s-underline-text'}).text
    except AttributeError:
        rating_cnt=''

    try:
        image = item.find('img',{'class' : 's-image'})
        imageSrc = image.get('src')
        print(imageSrc)
    except AttributeError:
        imageSrc = ""

    result = (description, price, rating, rating_cnt, prod_url,imageSrc)    
    return result

def extract_flipkart_record(item):
    atag = item.div.a
    prod_url = 'https://www.flipkart.com' + atag.get('href')  #product link
    page = urllib.request.urlopen(prod_url)
    soup = BeautifulSoup(page,'html.parser') 
    description = soup.find( class_ = 'B_NuCI').text.strip() # Will get text from html tags
    try:
        price = soup.find( class_ = '_30jeq3 _16Jk6d').get_text().strip()
    except:
        price = ''
    try:
        rating = soup.find( class_ = '_3LWZlK').get_text().strip()
    except:
        rating=''

    try:
        rating_cnt = soup.find( class_ = '_2_R_DZ').get_text().strip()
    except:
        rating_cnt=''

    try:
        print(soup.find('img', class_ = '_396cs4 _3exPp9'))
        print(soup.find('div', class_ = '_3ywSr_').div,"***********")
        div1 = soup.find('div', class_ = 'CXW8mj')
        div2 = soup.find('div', class_ = '_3ywSr_')
        if div1 is not None:
            imageSrc = div1.img['src']
        elif div2 is not None:
            imageSrc = div2.div.img['src']
        else :
            imageSrc = ""
    except AttributeError:
        imageSrc = ""
    result = (description, price, rating, rating_cnt, prod_url,imageSrc)
    return result    
    


def main(search_term):
    """Run main program routing"""
    #startup webdrive
    driver = webdriver.Chrome("C:/Users/ishas/Downloads/chromedriver_win32 (1)/chromedriver.exe",chrome_options=chrome_options)
    
    records = []
#     url = 'https://www.amazon.com'
    amz_url = get_amazon_url(search_term)
    #driver.get(url)

    driver.get(amz_url)
    record = ()
    #extract the collection
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    if(len(results)!=0):
        record = extract_amazon_record(results[0])
    if record:
        records.append(record)
    
    flip_url = get_flipkart_url(search_term)
    #driver.get(url)

    driver.get(flip_url)
    
    #extract the collection
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    results = soup.find_all('div', {'class': '_13oc-S'})
    if(len(results)!=0):
        record = extract_flipkart_record(results[0])
    if record and record not in records:
        records.append(record)

    driver.close()
    return records