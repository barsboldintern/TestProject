## Test File for Scraping data from a single real estate

from bs4 import BeautifulSoup

import requests
import pandas as pd
import time
home_url = 'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/'

# Function to get page content of the main page 

def get_page_content(home_url):
    #start = time.time()
    page = requests.get(home_url)
    page.raise_for_status()
    #end  = time.time()
    #elapsed_time = end - start
    #print("Elapsed time for get page content :", elapsed_time)
    return page
    
 # Function to extract ad links from the main page

def get_ad_links(main_page_url):
    #start = time.time()
    page = get_page_content(main_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    ad_links = []
    for link in soup.find_all('a', class_= 'mask'):
        href = link['href']
        if href.startswith('/adv/'):  # Adjust the pattern to match the ad links
            full_url = 'https://unegui.mn' + href  # Prepend the base URL to the relative URL
            ad_links.append(full_url)
    #end = time.time()
    #elapsed_time = end - start
    #print("Elapsed time for get ad links: ", elapsed_time)
    return ad_links

## Main function to scrape a single ad page

def get_info(link):
    #start = time.time()
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    char_price = soup.find('meta', itemprop ='price')
    price = char_price.get('content')
    char_title = soup.find_all('span', class_ = 'key-chars')
    char_address = soup.find('span', itemprop = 'address')
    address = char_address.text.strip()
    titles = [title.text.strip() for title in char_title]
    titles = ['үнэ']+  ['хаяг'] + titles 
    char_values = soup.find_all(class_ = 'value-chars')
    values = [value.text.strip() for value in char_values]
    values = [price] + [address] + values
    #end = time.time()
    #elapsed_time = end - start
    #print("Elapsed time for get info from a single page : ", elapsed_time)
    return titles, values

## Function to scrape all ad pages from the main page url
## @@param main_page_url = url of main page

def scrape_all_ads(main_page_url):
    #start = time.time()
    ad_links = get_ad_links(main_page_url)
    ads_data = []
    ads_titles = []
    for ad_link in ad_links:
        titles, values = get_info(ad_link)
        ads_data.append(values)
        ads_titles.append(titles)
    #end = time.time()
    #elapsed_time = end - start
    return ads_data, ads_titles

# Function to get all the feature from a main page url and prettify it.

def info_from_single(main_page_url):
    data, titles = scrape_all_ads(main_page_url)
    max_titles = max(titles, key=len)
    rows = []
    # Fill in the DataFrame rows with the corresponding values
    for ad_titles, ad_values in zip(titles, data):

        # Create a dictionary with empty strings for missing values

        row = {title: '' for title in max_titles}

        # Fill in the actual values for the titles present in the current ad

        for title, value in zip(ad_titles, ad_values):
            row[title] = value
        # Add the row dictionary to the list of rows
        rows.append(row)
    df = pd.DataFrame(rows, columns= max_titles)
    return df

## Function to get all prettified data from the first n page

def info_from_first_n(base_page_url, n):
    all_rows = []
    for i in range(1, n + 1):
        full_url = base_page_url + "?page=" + str(i - 1) if i != 1 else base_page_url
        try:
            sdf = info_from_single(full_url)  # Assuming you have a function called info_from_single
            all_rows.append(sdf)
        except Exception as e:
            print(f"Error encountered on page {i}: {e}")
            break  # Stop scraping if an error occurs
    if all_rows:
        df = pd.concat(all_rows, ignore_index=True)
        df.to_csv('oron_suuts.csv', index=False)
    else:
        print("No data scraped.")
    return

info_from_first_n(home_url, 100)

