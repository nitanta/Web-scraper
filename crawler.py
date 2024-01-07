import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

def classify_website(url):
    internal_links = set()
    external_links = set()

    base_url = urlparse(url).scheme + '://' + urlparse(url).hostname

    links = get_links(url)

    for link in links:
        full_url = urljoin(base_url, link)

        if base_url in full_url:
            internal_links.add(full_url)
        else:
            external_links.add(full_url)

    print(f"Number of internal links: {len(internal_links)}")
    for link in internal_links:
        print(f"{link}\n")
    print("..................................................")
    print(f"Number of external links: {len(external_links)}")
    for link in external_links:
        print(f"{link}\n")
    print("..................................................")

    if len(external_links) > len(internal_links):
        print("The website is a 'hub'.")
    else:
        print("The website is an 'authority'.")


classify_website("https://ekantipur.com")
