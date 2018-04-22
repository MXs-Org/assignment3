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
target_url = "http://google.com"

# Set of all visited links
all_links = set()

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
	else:
		# href starts with the proper protocol i.e. http or https
		return href

def pass_to_scanner(link, soup):
	# Final implementation is to pass URL to scanner once a link is found. 
	# For now, just print.
	scanner.scan(link, soup)

def crawler(url):
	# Input: string URL (host to crawl)
	# Output: string URL (links found)
	if url in all_links: 
		return

	# DFS recursive crawl
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	for a_element in soup.find_all('a', href=True):
		link = create_full_link(a_element['href'], url)
		if (link.startswith("http://") or link.startswith("https://")) and link not in all_links:
			all_links.add(link)
		 	pass_to_scanner(link, soup)
			try:
				crawler(link)
			except Exception:
				pass

if __name__ == "__main__":
	crawler(target_url)