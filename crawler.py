"""
Some lingo used in the files:
- page: a requests.models.Response object
- soup: a bs4.BeautifulSoup object, the result of BeautifulSoup(page.content, 'html.parser')
"""

import urlparse

import requests
from bs4 import BeautifulSoup

import scanner
from library import BASE_URL, TARGET_URL

def pass_to_scanner(link, soup):
	# Final implementation is to pass URL to scanner once a link is found. 
	# scanner.can returns a list of (vuln_class, result_obj)
	try:
		return scanner.scan(link, soup)
	except:
		return []

def create_full_link(href, url):
	return urlparse.urljoin(url, href)

def crawler(init_url):
	# FILO queue
	all_links = [init_url,]
	seen_links = {init_url}
	while all_links:
		url = all_links.pop()
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		# Scan the current URL for vulnerabilities
		pass_to_scanner(url, soup)
		# Find more links from the current URL
		for a_element in soup.find_all('a', href=True):
			link = create_full_link(a_element['href'], url)
			if BASE_URL not in link:
				# Discard any links that are not in the scanning scope
				continue	
			if link and link not in seen_links:
				seen_links.add(link)
				if link not in all_links:
					all_links.append(link)

if __name__ == "__main__":
	crawler(TARGET_URL)