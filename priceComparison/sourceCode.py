##putting it all together
import csv
from bs4 import BeautifulSoup
import urllib

#firefox & chrome
from selenium import webdriver

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
        return
    
    try:
        #rank and rating
        rating=item.i.text
        rating_cnt=item.find('span', {'class':'a-size-base s-underline-text'}).text
    except AttributeError:
        rating=''
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
        return
    try:
        rating = soup.find( class_ = '_3LWZlK').get_text().strip()
        rating_cnt = soup.find( class_ = '_2_R_DZ').get_text().strip()
    except:
        rating=''
        rating_cnt=''

    try:
       
        print(soup.find('img', class_ = '_396cs4 _3exPp9'))
        img = soup.find('div', class_ = 'CXW8mj').img
        print(img)
        #img = soup.find('img', class_ = '_396cs4 _3exPp9')
        if img :
            imageSrc = img['src']
        else :
            imageSrc = ""
    except AttributeError:
        imageSrc = ""
    result = (description, price, rating, rating_cnt, prod_url,imageSrc)
    return result    
    


def main(search_term):
    """Run main program routing"""
    #startup webdrive
    driver = webdriver.Chrome("C:/Users/ishas/Downloads/chromedriver_win32/chromedriver.exe")
    
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

    #driver.close()
    
    # #save data to csv file
    # with open('results.csv','w',newline='',encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
    #     writer.writerows(records)

    return records