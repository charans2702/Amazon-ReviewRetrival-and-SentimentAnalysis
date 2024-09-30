import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

headers = {
    'authority': 'www.amazon.in',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def reviewsHtml(base_url, product_id, len_page, max_retries=3, timeout=30):
    soups = []
    for page_no in range(1, len_page + 1):
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'pageNumber': page_no,
        }
       
        if page_no == 1:
            full_url = f"{base_url}{product_id}/ref=cm_cr_dp_d_show_all_btm"
        else:
            full_url = f"{base_url}{product_id}/ref=cm_cr_getr_d_paging_btm_next_{page_no}"
        
        retries = 0
        while retries < max_retries:
            try:
                logging.info(f"Attempting to scrape page {page_no}")
                response = requests.get(full_url, headers=headers, params=params, timeout=timeout)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'lxml')
                soups.append(soup)
                logging.info(f"Successfully scraped page {page_no}")
                time.sleep(random.uniform(5, 10)) 
                break  
            except requests.RequestException as e:
                logging.warning(f"Error scraping page {page_no} (attempt {retries + 1}): {e}")
                retries += 1
                if retries == max_retries:
                    logging.error(f"Failed to scrape page {page_no} after {max_retries} attempts")
                    if page_no == 1:
                        logging.error("Failed to scrape the first page. Stopping the script.")
                        return []
                    return soups  
                time.sleep(random.uniform(10, 20)) 
    return soups

def getReviews(html_data):
    data_dicts = []
    boxes = html_data.select('div[data-hook="review"]')
    logging.info(f"Found {len(boxes)} review boxes on this page")
    
    for box in boxes:
        try:
            title_element = box.select_one('[data-hook="review-title"]')
            title = title_element.text.strip().split('\n')[-1] if title_element else 'N/A'
        except Exception as e:
            logging.warning(f"Error extracting title: {e}")
            title = 'N/A'
        
        try:
            description_element = box.select_one('[data-hook="review-body"]')
            description = description_element.text.strip() if description_element else 'N/A'
        except Exception as e:
            logging.warning(f"Error extracting description: {e}")
            description = 'N/A'
        
        try:
            rating_element = box.select_one('i[data-hook="review-star-rating"]')
            rating = rating_element.text.strip().split(' ')[0] if rating_element else 'N/A'
        except Exception as e:
            logging.warning(f"Error extracting rating: {e}")
            rating = 'N/A'
        
        try:
            format_strip = box.select_one('.review-format-strip')
            color = format_strip.find(string=lambda t: 'Colour:' in t).split(':')[1].strip()
        except Exception as e:
            color = 'N/A'
        
        try:
            format_strip = box.select_one('.review-format-strip')
            size = format_strip.find(string=lambda t: 'Size:' in t).split(':')[1].strip()
        except Exception as e:
            size = 'N/A'
        
        try:
            verified = box.select_one('[data-hook="avp-badge"]').text.strip()
        except Exception as e:
            verified = 'Not Verified'
        
        
        data_dict = {
            'Title': title,
            'Description': description,
            'Rating': rating,
            'Color':color,
            'Storage Size':size,
            'Verified Purchase':verified

        }
        
        data_dicts.append(data_dict)
    
    return data_dicts


def save_to_database(reviews):
    df = pd.DataFrame(reviews)
    engine = create_engine('sqlite:///amazon_reviews.db')
    df.to_sql('reviews', engine, if_exists='replace', index=False)


if __name__=='__main__':
    base_url = 'https://www.amazon.in/New-Apple-iPhone-12-128GB/product-reviews/'
    product_id = 'B08L5TNJHG'
    len_page = 15
    html_datas = reviewsHtml(base_url, product_id, len_page)
    reviews = []
    for html_data in html_datas:
        review = getReviews(html_data)
        reviews += review
    print(f"Scraped {len(reviews)} reviews")
    save_to_database(reviews)
    print('Successfully saved to database')
