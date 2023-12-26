import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_image_urls(page_url):
    # Send a GET request to the page
    response = requests.get(page_url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parse the page's content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <img> tags on the page
    img_tags = soup.find_all('img')

    # List to hold image URLs
    urls = []

    # Extract the 'src' attribute of each <img> tag
    for img in img_tags:
        img_url = img.get('src')
        # Convert relative URLs to absolute URLs
        img_url = urljoin(page_url, img_url)
        urls.append(img_url)

    return urls[1]

# # Usage
# page_url = 'https://torob.com/p/be663199-b7c5-4f2e-b93c-a5913e6298e5/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-vivobook-s-15-oled-k3502za-z/'

# # Get all image URLs from the webpage
# image_urls = get_image_urls(page_url)
# print(image_urls)