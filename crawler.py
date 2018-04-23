"""
Some lingo used in the files:
- page: a requests.models.Response object
- soup: a bs4.BeautifulSoup object, the result of BeautifulSoup(page.content, 'html.parser')
"""

import requests
from bs4 import BeautifulSoup

import scanner

# Modify this
# TODO: maybe change this to be a command line argument?
# Note: DON'T end with a TRAILING '/'
target_url = "http://localhost:8888"

def pass_to_scanner(link, soup):
	# Final implementation is to pass URL to scanner once a link is found. 
	# For now, just print.
	scanner.scan(link, soup)

def create_full_link(href, url):
	# Checks if href is a relative or absolute URL. 
	# Returns the fully qualified URL i.e. http://target.com/foo/bar
	# TODO: what if there are weird things like "../"?
	if href[0] == '/':
		# Relative link
		return url + href
	elif href[0] == '.':
		# Weird relative link, need to remove period
		return url + href[1:]
	elif not (href.startswith("http://") or href.startswith("https://")):
		# Relative link
		return url + "/" + href
	else:
		# href starts with the proper protocol i.e. http or https
		return href

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
			if link not in seen_links:
				seen_links.add(link)
				if link not in all_links:
					all_links.append(link)

if __name__ == "__main__":
	crawler(target_url)