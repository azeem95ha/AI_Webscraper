from bs4 import BeautifulSoup
import requests
import re

def get_clean_html_content(url):
    print("Cleaning the HTML content...")
    # Fetch the HTML content from the URL
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page content: Status code {response.status_code}")

    html_content = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove specific tags: [meta, script, header, footer, style]
    for tag_name in ['meta', 'script', 'header', 'footer', 'style', 'link', 'title', 'noscript', 'head', 'pubguru', 'iframe', 'svg', 'path']:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Iterate through all tags and clean them
    for tag in soup.find_all(True):
        # Preserve only 'class' and 'id' attributes, remove all other attributes
        attributes_to_keep = {k: tag.attrs[k] for k in ('class', 'id') if k in tag.attrs}
        tag.attrs = attributes_to_keep
        
        # Remove the text content of the tag but keep the tag itself
        for content in tag.find_all(text=True, recursive=False):
            content.extract()

    # Return the cleaned HTML
    cleaned_html = soup.prettify()
    print("The HTML content has been cleaned successfully.")
    return cleaned_html


