""" Script for extracting all links and their innerHtml content present on the given webpage url
    and writes them to hyperlinks.json file
    install requirements
    pip install beautifulsoup4 requests
"""
import json, re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time

def get_all_hyperlinks(website_url):
    hyperlinks = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = requests.get(url=website_url, headers=headers)
        time.sleep(2)
        if not req.status_code == 200:
            raise Exception('Website blocked request')
        
        # Parse the HTML content
        soup = BeautifulSoup(req.text, 'html.parser')

        # Find all <a> tags which represent hyperlinks
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            text = link.get_text()
            text = ' '.join(re.findall('[a-z|A-Z]+', text))

            # Join the URL if the link is relative
            full_url = urljoin(website_url, href)
            hyperlinks.append({'url': full_url, 'text':text})
    except Exception as e:
        print(f"error occurred -> {str(e)}")
    return hyperlinks

def get_webpage_text(website_url):
    data = {}
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = requests.get(url=website_url, headers=headers)
        time.sleep(2)
        if not req.status_code == 200:
            raise Exception('Website blocked request')
        
        # Parse the HTML content
        soup = BeautifulSoup(req.text, 'html.parser')

        #Remove all css heading title javascript tags/elements
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        text = soup.get_text()
        
        data = {
            'text' : ' '.join(re.findall('[a-z|A-Z]+', text)),
            'url': website_url
        }
    except Exception as e:
        print(f"error occurred -> {str(e)}")
    return data



# Example usage:
if __name__ == "__main__":
    # website_url = input("Enter website URL: ")
    website_url = "https://paperswithcode.com/"
    print(f" Scraping --> {website_url}")
    hyperlinks = get_all_hyperlinks(website_url)
    print("text scrap")
    get_text = get_webpage_text(website_url)

    if hyperlinks:
        with open('hyperlinks.json', 'w+') as json_file:
            json.dump(hyperlinks, json_file, indent=4)
        print("Hyperlinks saved to hyperlinks.json")
    if get_text:
        with open('webpage_text.json', 'w+') as json_file:
            json.dump(get_text, json_file, indent=4)
        print("text data saved to webpage_text.json")