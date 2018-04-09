import requests
from bs4 import BeautifulSoup

target_url = "localhost"
all_links = set()

def create_full_link(href, URL):
	return URL + href if href[0] == '/' else href

def pass_to_scanner(link):
	#Final implementation is to pass URL to scanner once a link is found. 
	#For now, just print.
	print(link)

def crawler(URL):
	#Input: string URL (host to crawl)
	#Output: string URL (links found)
	
	if URL in all_links: return

	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')

	for a_element in soup.find_all('a', href=True):
		link = create_full_link(a_element['href'], URL)

		if (link.startswith("http://") or link.startswith("https://")) and link not in all_links:
			all_links.add(link)
		 	pass_to_scanner(link)
		
			try:
				crawler(link)
			except Exception:
				pass

crawler(target_url)